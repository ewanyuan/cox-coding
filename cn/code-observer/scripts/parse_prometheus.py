#!/usr/bin/env python3
"""
解析Prometheus指标数据，提取性能指标
"""

import json
import re
import sys
import argparse
from typing import Dict, List, Any, Tuple


class PrometheusParser:
    """Prometheus指标解析器"""
    
    def __init__(self, prom_file: str):
        self.prom_file = prom_file
        self.parsed_metrics = {
            "gauge_metrics": [],
            "counter_metrics": [],
            "histogram_metrics": [],
            "summary_metrics": [],
            "summary": {}
        }
    
    def parse(self) -> Dict[str, Any]:
        """解析Prometheus指标文件"""
        try:
            with open(self.prom_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析各个指标类型
            self._parse_metrics(content)
            
            # 生成摘要
            self._generate_summary()
            
            return self.parsed_metrics
            
        except FileNotFoundError:
            raise Exception(f"Prometheus指标文件不存在: {self.prom_file}")
        except Exception as e:
            raise Exception(f"解析Prometheus指标失败: {str(e)}")
    
    def _parse_metrics(self, content: str):
        """解析指标"""
        lines = content.strip().split('\n')
        
        current_metric = None
        metric_type = None
        
        for line in lines:
            line = line.strip()
            
            # 跳过注释和空行
            if not line or line.startswith('#'):
                # 检查指标类型注释
                if line.startswith('# TYPE'):
                    parts = line.split()
                    if len(parts) >= 3:
                        current_metric = parts[2]
                        metric_type = parts[3] if len(parts) > 3 else 'unknown'
                continue
            
            # 解析指标行
            self._parse_metric_line(line, metric_type)
    
    def _parse_metric_line(self, line: str, metric_type: str):
        """解析单行指标"""
        # 匹配指标名称和值
        match = re.match(r'^([a-zA-Z_:][a-zA-Z0-9_:]*)(?:\{([^}]*)\})?\s+([+-]?\d+\.?\d*(?:[eE][+-]?\d+)?)', line)
        
        if not match:
            return
        
        metric_name = match.group(1)
        labels_str = match.group(2) if match.group(2) else ''
        value = float(match.group(3))
        
        # 解析标签
        labels = self._parse_labels(labels_str)
        
        metric_data = {
            "name": metric_name,
            "value": value,
            "labels": labels,
            "timestamp": ""
        }
        
        # 根据指标类型分类
        if metric_type == 'gauge':
            self.parsed_metrics["gauge_metrics"].append(metric_data)
        elif metric_type == 'counter':
            self.parsed_metrics["counter_metrics"].append(metric_data)
        elif metric_type == 'histogram':
            self.parsed_metrics["histogram_metrics"].append(metric_data)
        elif metric_type == 'summary':
            self.parsed_metrics["summary_metrics"].append(metric_data)
        else:
            # 默认归为gauge
            self.parsed_metrics["gauge_metrics"].append(metric_data)
    
    def _parse_labels(self, labels_str: str) -> Dict[str, str]:
        """解析标签字符串"""
        labels = {}
        if not labels_str:
            return labels
        
        # 简单解析 key="value" 格式
        pairs = re.findall(r'(\w+)="([^"]*)"', labels_str)
        for key, value in pairs:
            labels[key] = value
        
        return labels
    
    def _generate_summary(self):
        """生成摘要信息"""
        self.parsed_metrics["summary"] = {
            "total_gauge_metrics": len(self.parsed_metrics["gauge_metrics"]),
            "total_counter_metrics": len(self.parsed_metrics["counter_metrics"]),
            "total_histogram_metrics": len(self.parsed_metrics["histogram_metrics"]),
            "total_summary_metrics": len(self.parsed_metrics["summary_metrics"]),
            "metric_names": list(set([
                m["name"] for m in
                self.parsed_metrics["gauge_metrics"] +
                self.parsed_metrics["counter_metrics"] +
                self.parsed_metrics["histogram_metrics"] +
                self.parsed_metrics["summary_metrics"]
            ]))
        }


def main():
    parser = argparse.ArgumentParser(description='解析Prometheus指标数据')
    parser.add_argument('--prom-file', required=True, help='Prometheus指标文件路径')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        prom_parser = PrometheusParser(args.prom_file)
        parsed_data = prom_parser.parse()
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        
        print(f"Prometheus指标解析完成，输出文件: {args.output}")
        print(f"Gauge指标: {parsed_data['summary']['total_gauge_metrics']}")
        print(f"Counter指标: {parsed_data['summary']['total_counter_metrics']}")
        print(f"Histogram指标: {parsed_data['summary']['total_histogram_metrics']}")
        print(f"Summary指标: {parsed_data['summary']['total_summary_metrics']}")
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
