// 基本库
#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <algorithm>
#include <string.h>

// STL容器
#include <vector>
#include <set>
#include <map>

// 错误码
#define FILE_OPEN_ERROE 1
#define LEXICAL_ERROR_UNDEFINED_WORD 2

using namespace std;

// 标识符
struct TOKEN
{
	string token; // token类型
	string value; // 值
	int row;	  // 行
	int col;	  // 列
};

// 词法分析的类
class lexical_analysis
{
private:
	// 标识符流（使用vector的原因是只需在末尾添加，查找快）
	vector<TOKEN> token_stream;

public:
	// 删除默认构造函数
	lexical_analysis() = delete;
	// 构造函数，输入文件路径
	lexical_analysis(const string file_path);
	// 析构函数
	~lexical_analysis() {}
	// 将结果输出到文件
	void print_token_stream(const string file_path);
	// 得到token_stream
	vector<TOKEN> get_token_stream();
};

// 标识符的定义
// 关键字（使用set的原因是为了确保唯一性）
const set<string> Keyword = {"int", "void", "if", "else", "while", "return", "for", "do", "break", "continue", "float", "double"}; // 将float和double都输出为double
// 分隔符
const set<string> Separator = {",", ";", "(", ")", "{", "}", "[", "]"};
// 运算符
const set<string> Operator_1 = {"+", "-", "*", "/", "=", ">", "<", "%", "!"};
const set<string> Operator_2 = {"==", ">=", "<=", "!=", "->", "++", "--", "+=", "-=", "*=", "/=", "%=", "||", "&&"};

const string Identifier = "ID";

const string ConstInt = "NUM";
const string ConstFloat_or_double = "NUM";

// 将所有符号都插入进一个集合中
set<string> InsertTokens()
{
	set<string> temp;
	temp.insert(Keyword.begin(), Keyword.end());
	temp.insert(Separator.begin(), Separator.end());
	temp.insert(Operator_1.begin(), Operator_1.end());
	temp.insert(Operator_2.begin(), Operator_2.end());
	temp.insert(Identifier);
	temp.insert(ConstInt);
	return temp;
}
const set<string> AllTokens = move(InsertTokens());

// 构造函数，输入文件路径
lexical_analysis::lexical_analysis(const string file_path)
{
	// 打开文件
	ifstream file_in;
	file_in.open(file_path, ios::in | ios::binary);

	// 未打开文件则抛出异常
	if (!file_in.is_open())
	{
		cout << "无法打开源代码文件" << endl;
		throw FILE_OPEN_ERROE;
	}

	// present_row为当前行数
	int present_row = 1;
	// present_col为当前列数
	int present_col = 0;
	// 当前字符串
	string present_str;
	// 当前字符
	char present_ch;
	// 开始进行识别
	while (file_in.peek() != EOF)
	{
		present_ch = char(file_in.get());
		present_col++;
		// cout<<present_ch<<endl;
		// 如果为空格
		if (isspace(present_ch))
		{
			if (present_ch == '\n')
			{
				present_row++;
				present_col = 0;
			}
			else if (present_ch == '\t')
			{
				present_col += 3;
			}
			continue;
		}
		// 如果不是空格
		present_str = present_ch;

		// 如果是字母
		if (isalpha(present_ch))
		{
			// 如果下一个字符是数字或字母
			while (isalnum(present_ch = char(file_in.get())))
			{
				present_str += present_ch;
				present_col++;
			}

			// 倒回去一个字符
			file_in.seekg(-1, ios::cur);
			// 检查是不是保留字
			if (Keyword.find(present_str) != Keyword.cend())
				token_stream.push_back({present_str, present_str, present_row, present_col - int(present_str.length()) + 1});
			else // 不是保留字
				token_stream.push_back({Identifier, present_str, present_row, present_col - int(present_str.length()) + 1});
		}
		// 如果是数字
		else if (isdigit(present_ch))
		{
			// 如果下一个字符是数字
			while (isdigit(present_ch = char(file_in.get())))
			{
				present_str += present_ch;
				present_col++;
			}
			if (present_ch == '.')
			{ // 可能是小数
				if (isdigit(present_ch = char(file_in.get())))
				{ // 下一个是数字就一定是小数了
					present_str += '.';
					present_str += present_ch;
					present_col++;
					while (isdigit(present_ch = char(file_in.get())))
					{
						present_str += present_ch;
						present_col++;
					}
					// 倒回去一个字符
					file_in.seekg(-1, ios::cur);
					// 插入token_stream
					token_stream.push_back({ConstFloat_or_double, present_str, present_row, present_col - int(present_str.length()) + 1});
					continue;
				}
				// 倒回去一个字符
				file_in.seekg(-1, ios::cur);
			}
			// 倒回去一个字符
			file_in.seekg(-1, ios::cur);
			// 插入token_stream
			token_stream.push_back({ConstInt, present_str, present_row, present_col - int(present_str.length()) + 1});
		}
		// 如果是分隔符
		else if (Separator.find(present_str) != Separator.cend())
			token_stream.push_back({present_str, present_str, present_row, present_col});
		// 如果是单行注释
		else if (present_ch == '/' && file_in.peek() == '/')
		{
			while (char(file_in.get()) != '\n')
				;
			present_row++;
			present_col = 0;
		}
		// 如果是多行注释
		else if (present_ch == '/' && file_in.peek() == '*')
		{
			while (!((present_ch = char(file_in.get())) == '*' && char(file_in.peek()) == '/'))
			{
				present_col++;
				if (present_ch == '\n')
				{
					present_row++;
					present_col = 0;
				}
				else if (present_ch == '\t')
					present_col += 3;
			}
			file_in.get();
			present_col += 2;
		}
		// 如果是两个个字符的运算符（先检查是不是两个再检查一个）
		else if (Operator_2.find(present_str + char(file_in.peek())) != Operator_2.cend())
		{
			present_str += char(file_in.get());
			present_col++;
			token_stream.push_back({present_str, present_str, present_row, present_col - 1});
		}
		// 如果是一个字符的运算符
		else if (Operator_1.find(present_str) != Operator_1.cend())
			token_stream.push_back({present_str, present_str, present_row, present_col});
		else
		{
			cout << "识别到无法识别的字符，在第" << present_row << "行，第" << present_col << "列" << endl;
			throw LEXICAL_ERROR_UNDEFINED_WORD;
		}
	}
}
// 将结果输出到文件
void lexical_analysis::print_token_stream(const string file_path)
{
	ofstream file_out;
	file_out.open(file_path, ios::out);
	for (auto it = token_stream.begin(); it != token_stream.end(); it++)
	{
		file_out << (*it).row << ' ' << (*it).token << ' ' << (*it).value<<endl;
	}
}
// 得到token_stream
vector<TOKEN> lexical_analysis::get_token_stream()
{
	return token_stream;
}

int main(int argc, char *argv[])
{
	try
	{
		string test_code_file_path = argv[1];
		// string test_code_file_path = "./input/input.c";
		lexical_analysis lexicalAnalysis(test_code_file_path);
		lexicalAnalysis.print_token_stream("./output/lexical_analysis.txt");
	}
	catch (int e)
	{
		printf("error code: %d", e);
		return e;
	}
	return 0;
}
