#!/usr/bin/env python3
"""
解析结构化可观测日志，提取执行路径、函数调用、异常信息
"""

import json
import re
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional


class LogParser:
    """日志解析器，提取执行路径、函数调用与异常信息"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.parsed_data = {
            "execution_paths": [],
            "function_calls": [],
            "exceptions": [],
            "summary": {}
        }
    
    def parse(self) -> Dict[str, Any]:
        """解析日志文件"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 尝试解析JSON格式日志
            if self._is_json_log(content):
                self._parse_json_logs(content)
            else:
                # 解析文本格式日志
                self._parse_text_logs(content)
            
            # 生成摘要信息
            self._generate_summary()
            
            return self.parsed_data
            
        except FileNotFoundError:
            raise Exception(f"日志文件不存在: {self.log_file}")
        except Exception as e:
            raise Exception(f"解析日志失败: {str(e)}")
    
    def _is_json_log(self, content: str) -> bool:
        """判断是否为JSON格式日志"""
        lines = content.strip().split('\n')
        if not lines:
            return False
        try:
            json.loads(lines[0])
            return True
        except json.JSONDecodeError:
            return False
    
    def _parse_json_logs(self, content: str):
        """解析JSON格式日志"""
        lines = content.strip().split('\n')
        
        for line in lines:
            try:
                entry = json.loads(line.strip())
                
                # 提取执行路径
                if 'trace_id' in entry or 'span_id' in entry:
                    self.parsed_data["execution_paths"].append({
                        "trace_id": entry.get('trace_id', ''),
                        "span_id": entry.get('span_id', ''),
                        "parent_id": entry.get('parent_id', ''),
                        "timestamp": entry.get('timestamp', ''),
                        "level": entry.get('level', 'INFO'),
                        "message": entry.get('message', '')
                    })
                
                # 提取函数调用
                if 'function' in entry or 'method' in entry:
                    self.parsed_data["function_calls"].append({
                        "timestamp": entry.get('timestamp', ''),
                        "function": entry.get('function', entry.get('method', '')),
                        "duration_ms": entry.get('duration_ms', 0),
                        "args": entry.get('args', {}),
                        "result": entry.get('result', None),
                        "level": entry.get('level', 'INFO')
                    })
                
                # 提取异常信息
                if 'exception' in entry or 'error' in entry or entry.get('level') in ['ERROR', 'CRITICAL']:
                    self.parsed_data["exceptions"].append({
                        "timestamp": entry.get('timestamp', ''),
                        "level": entry.get('level', 'ERROR'),
                        "exception_type": entry.get('exception', {}).get('type', 'Unknown'),
                        "exception_message": entry.get('exception', {}).get('message', entry.get('error', '')),
                        "stack_trace": entry.get('exception', {}).get('stack_trace', ''),
                        "context": entry.get('context', {})
                    })
                    
            except json.JSONDecodeError:
                continue
    
    def _parse_text_logs(self, content: str):
        """解析文本格式日志"""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析时间戳（尝试多种格式）
            timestamp = self._extract_timestamp(line)
            
            # 解析日志级别
            level = self._extract_log_level(line)
            
            # 解析函数调用
            if 'call' in line.lower() or 'exec' in line.lower():
                function_match = re.search(r'function[:\s]+(\w+)', line, re.IGNORECASE)
                if function_match:
                    duration_match = re.search(r'duration[:\s]+(\d+(?:\.\d+)?)\s*ms', line, re.IGNORECASE)
                    self.parsed_data["function_calls"].append({
                        "timestamp": timestamp,
                        "function": function_match.group(1),
                        "duration_ms": float(duration_match.group(1)) if duration_match else 0,
                        "level": level,
                        "raw_line": line
                    })
            
            # 解析异常
            if 'error' in line.lower() or 'exception' in line.lower() or level in ['ERROR', 'CRITICAL']:
                exception_type_match = re.search(r'(\w+Error|\w+Exception)', line)
                self.parsed_data["exceptions"].append({
                    "timestamp": timestamp,
                    "level": level,
                    "exception_type": exception_type_match.group(1) if exception_type_match else 'Unknown',
                    "exception_message": line,
                    "stack_trace": '',
                    "context": {}
                })
            
            # 默认添加到执行路径
            if timestamp and level:
                self.parsed_data["execution_paths"].append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": line,
                    "trace_id": '',
                    "span_id": ''
                })
    
    def _extract_timestamp(self, line: str) -> Optional[str]:
        """提取时间戳"""
        # 尝试常见时间戳格式
        patterns = [
            r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?',  # ISO格式
            r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}',  # MM/DD/YYYY格式
            r'\[\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\]',  # 带括号格式
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_log_level(self, line: str) -> str:
        """提取日志级别"""
        levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE']
        line_upper = line.upper()
        
        for level in levels:
            if level in line_upper:
                return level
        
        return 'INFO'
    
    def _generate_summary(self):
        """生成摘要信息"""
        self.parsed_data["summary"] = {
            "total_execution_paths": len(self.parsed_data["execution_paths"]),
            "total_function_calls": len(self.parsed_data["function_calls"]),
            "total_exceptions": len(self.parsed_data["exceptions"]),
            "error_count": len([e for e in self.parsed_data["exceptions"] if e["level"] in ['ERROR', 'CRITICAL']]),
            "avg_duration_ms": 0,
            "max_duration_ms": 0
        }
        
        # 计算耗时统计
        durations = [fc["duration_ms"] for fc in self.parsed_data["function_calls"] if fc["duration_ms"] > 0]
        if durations:
            self.parsed_data["summary"]["avg_duration_ms"] = sum(durations) / len(durations)
            self.parsed_data["summary"]["max_duration_ms"] = max(durations)


def main():
    parser = argparse.ArgumentParser(description='解析结构化可观测日志')
    parser.add_argument('--log-file', required=True, help='日志文件路径')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        log_parser = LogParser(args.log_file)
        parsed_data = log_parser.parse()
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        
        print(f"日志解析完成，输出文件: {args.output}")
        print(f"执行路径: {parsed_data['summary']['total_execution_paths']}")
        print(f"函数调用: {parsed_data['summary']['total_function_calls']}")
        print(f"异常数量: {parsed_data['summary']['total_exceptions']}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
