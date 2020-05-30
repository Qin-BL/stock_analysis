# -*- coding: UTF-8 -*-


def get_html_msg(up_list):
    # 表格格式
    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse:collapse;
                    border: 2px solid #a19da2;
                    /*默认居中auto显示整个表格*/
                    margin: left
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {
                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td{
                    text-align: left;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 宋体；
                }

                h1 {
                    color: #5db446
                    }

                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5pxx #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0,2,227,0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239,241,234,0.99);
                    line-height; 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }

            </style>

        </head>
        """

    # 构造正文表格
    body = """
         <body>
             <div class="content">
                {df_html}
             </div>
         </body>
         <br /><br />
        """
    tb_html = """<table border="1" class="dataframe">
                  <thead>
                    <tr style="text-align: right;">
                      <th>代码</th>
                      <th>名称</th>
                      <th>详情</th>
                      <th>公告时间</th>
                      <th>涨幅</th>
                    </tr>
                  </thead>
                  <tbody>
                    %s
                  </tbody>
                </table>"""
    all_tr = ''
    for i in up_list:
        all_tr += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="color: red;">%.2f%%</td></tr>' % \
                  (i['code'], i['name'], i['detials'], i['notice_time'], i['range'])
    html_msg = "<html>" + head + body.format(df_html=tb_html % all_tr) + "</html>"
    return html_msg
