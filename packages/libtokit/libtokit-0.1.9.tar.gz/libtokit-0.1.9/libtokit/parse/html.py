import xml.etree.ElementTree as ET
import json


class ProblemParser:
    """一个用于解析 Online Judge 题目 XML 文件的解析器。"""

    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.problems = []

    def parse(self):
        """解析 XML 文件，并将结果保存在实例变量中。"""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            self.problems = [self._parse_item(item) for item in root.findall('item')]
        except ET.ParseError as e:
            print(f"XML 解析错误: {e}")
            return None

    def _parse_item(self, item):
        """解析单个题目项，并返回字典格式的数据。"""
        return {
            "title": self._extract_text(item, 'title'),
            "time_limit": self._extract_text(item, 'time_limit') + item.find('time_limit').get('unit', ''),
            "memory_limit": self._extract_text(item, 'memory_limit') + item.find('memory_limit').get('unit', ''),
            "description": self._extract_text(item, 'description'),
            "input": self._extract_text(item, 'input'),
            "output": self._extract_text(item, 'output'),
            "sample_input": self._extract_text(item, 'sample_input'),
            "sample_output": self._extract_text(item, 'sample_output'),
            "test_cases": self._extract_test_cases(item),
            "source": self._extract_text(item, 'source'),
            "solutions": self._extract_solutions(item)
        }

    @staticmethod
    def _extract_text(element, tag, default=""):
        """提取 XML 标签的文本内容，若不存在则返回默认值。"""
        return element.findtext(tag, default).strip()

    @staticmethod
    def _extract_test_cases(item):
        """提取测试用例，并返回列表格式的数据。"""
        test_cases = []
        for test_input in item.findall('test_input'):
            name = test_input.get('name', '')
            input_data = test_input.text.strip()
            output_element = item.find(f"test_output[@name='{name}']")
            output_data = output_element.text.strip() if output_element is not None else ""
            test_cases.append({"input": input_data, "output": output_data})
        return test_cases

    @staticmethod
    def _extract_solutions(item):
        """提取各语言的代码实现，并返回字典格式的数据。"""
        solutions = {}
        for solution in item.findall('solution'):
            language = solution.get('language', '').strip()
            code = solution.text.strip()
            solutions[language] = code
        return solutions

    def to_json(self):
        """将解析结果转换为 JSON 字符串格式。"""
        return json.dumps(self.problems, ensure_ascii=False, indent=4)


# 使用示例
if __name__ == "__main__":
    xml_file = 'test.xml'  # 替换为实际 XML 文件路径
    parser = ProblemParser(xml_file)  # 初始化解析器
    parser.parse()  # 解析 XML 文件
    parsed_data = parser.to_json()  # 转换为 JSON 格式
    if parsed_data:
        print(parsed_data)  # 打印 JSON 数据
