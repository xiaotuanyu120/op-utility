#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xlsxwriter


class HostStatistics(object):
    """用来统计ansible批量fetch回来的巡检文件"""
    def __init__(self, base, remote_file, xlsx_file):
        """
        base是本地储存fetch文件的根目录
        remote_file是服务器端的文件绝对路径
        xlsx_file是本地生成的结果保存xlsx文件位置
        """
        self.base = base
        self.remote_file = remote_file
        self.xlsx_file = xlsx_file

    def host_list(self):
        """返回ansible中的主机ip或别名列表"""
        return [x for x in os.listdir(self.base) if os.path.isdir(self.base+x)]

    def host_state(self, host_name):
        """返回主机ip或别名文件夹中的文件内容"""
        local_file = "%s/%s/%s" % (self.base, host_name, self.remote_file)
        with open(local_file) as f:
            host_state = ''.join(f.readlines())
        return host_state

    def xlsx_write(self):
        """将结果输出到excel文件中"""
        # 创建文件和sheet
        workbook = xlsxwriter.Workbook(self.xlsx_file)
        worksheet = workbook.add_worksheet()
        # 格式化
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 50)
        format = workbook.add_format()
        format.set_text_wrap()
        format.set_align('vcenter')
        for i in range(len(self.host_list())):
            num = str(i+1)
            row_col_A = 'A' + num
            host_name = self.host_list()[i]
            worksheet.write(row_col_A, host_name, format)

            row_col_B = 'B' + num
            host_state = self.host_state(host_name)
            worksheet.write(row_col_B, host_state, format)


if __name__ == "__main__":
    check_base = "/tmp/check_host_result/"
    remote_file = "/tmp/check_host.txt"
    xslx_file = "check_host.xlsx"
    hs = HostStatistics(check_base, remote_file, xslx_file)
    hs.xlsx_write()
