
+++
date = "2007-12-21"
draft = false
title = """Google Chart API, Wow!"""
slug = "google-chart-api-wow"
tags = ['Software Development']
banner = ""
aliases = ['/google-chart-api-wow/']
+++


I have always been a sucker for statistical eye candy. Last week Google launched their chart APIs. I have always done charts client-side with a java applet or SWF application. Server-side solutions where always kludgey. They required way to much customization and each provider/chart style had a different interface. Thanks to Google, static charts are now super simple. The API currently supports line, bar, pie charts, venn diagrams and scatter plots. Most of the standard Google API rules apply. You are going to see these popping up all over the place. I know I am definitely going to give them a try.  
 this -

```
http://chart.apis.google.com/chart?cht=lc&chd=s:cEAELFJHHHKU<br></br>
ju9uuXUc&chco=76A4FB&chls=2.0,0.0,0.0&chs=200x125&chg=20,50,<br></br>
1,0&chxt=x,y&chxl=0:|0|1|2|3|4|5|1:|0|50|100<br></br>```
  
 - turns into this -  
![Google Chart](http://chart.apis.google.com/chart?cht=lc&chd=s:cEAELFJHHHKUju9uuXUc&chco=76A4FB&chls=2.0,0.0,0.0&chxt=x,y&chxl=0:|0|1|2|3|4|5|1:|0|50|100&chs=400x250&chg=20,50,1,5)  
 - beautiful isn-t it.




