#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ebay's scrapping category
# Description: Script to download ebay's category structure into SQLITE and Render Structure into HTML file.
#
# Usage: 
#		python ebay_categories_api.py --rebuild
#		python ebay_categories_api.py --render 179022
#		python ebay_categories_api.py --render 179022
#		
# name: ebay_categories_api.py
# Autor: Felix E. Orduz G. - <felix.orduz@gmail.com>

import argparse
import sqlite3
import requests
import xml.etree.ElementTree as ET

#Constants
html_template_header = '<!doctype html><html><head> <title>CSS3 ordered list styles - demo</title> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> <style>h1,h3{font-weight:700}.rectangle-list a,.rounded-list a{display:block;color:#444;text-decoration:none}.fa,.rectangle-list a,.rounded-list a{text-decoration:none}body{margin:40px auto;width:500px}h1{font-family:times,Times New Roman,times-roman,georgia,serif;color:#444;margin:0;padding:0 0 6px;font-size:51px;line-height:44px;letter-spacing:-2px}h3{font-family:Gill Sans,Verdana;font-size:11px;line-height:14px;text-transform:uppercase;letter-spacing:2px}ul{counter-reset:li;list-style:none;font:15px \'trebuchet MS\',\'lucida sans\';padding:0;margin-bottom:4em;text-shadow:0 1px 0 rgba(255,255,255,.5)}.rectangle-list a:before,.rounded-list a:before{content:close-quote;height:2em;width:2em;line-height:2em;font-weight:700;top:50%;counter-increment:li;text-align:center}ul ul{margin:0 0 0 2em}.rounded-list a{position:relative;padding:.4em .4em .4em 2em;margin:.5em 0;background:#ddd;-moz-border-radius:.3em;-webkit-border-radius:.3em;border-radius:.3em;-webkit-transition:all .3s ease-out;-moz-transition:all .3s ease-out;-ms-transition:all .3s ease-out;-o-transition:all .3s ease-out;transition:all .3s ease-out}.rectangle-list a,.rounded-list a:before{-webkit-transition:all .3s ease-out;-moz-transition:all .3s ease-out;-ms-transition:all .3s ease-out;-o-transition:all .3s ease-out}.rounded-list a:hover{background:#eee}.rounded-list a:hover:before{-webkit-transform:rotate(360deg);-moz-transform:rotate(360deg);-ms-transform:rotate(360deg);-o-transform:rotate(360deg);transform:rotate(360deg)}.rounded-list a:before{position:absolute;left:-1.3em;margin-top:-1.3em;background:#87ceeb;border:.3em solid #fff;-moz-border-radius:2em;-webkit-border-radius:2em;border-radius:2em;transition:all .3s ease-out}.rectangle-list a{position:relative;padding:.4em .4em .4em .8em;margin:.5em 0 .5em 2.5em;background:#ddd;transition:all .3s ease-out}.rectangle-list a:hover{background:#eee}.rectangle-list a:before{position:absolute;left:-2.5em;margin-top:-1em;background:salmon}.rectangle-list a:after{position:absolute;content:\'\';border:.5em solid transparent;left:-1em;top:50%;margin-top:-.5em;-webkit-transition:all .3s ease-out;-moz-transition:all .3s ease-out;-ms-transition:all .3s ease-out;-o-transition:all .3s ease-out;transition:all .3s ease-out}.rectangle-list a:hover:after{left:-.5em;border-left-color:salmon}.circle-list li{padding:2.5em;border-bottom:1px dashed #ccc}.circle-list h2{position:relative;margin:0}.circle-list p{margin:0}.circle-list h2:before{content:counter(li);counter-increment:li;position:absolute;z-index:-1;left:-1.3em;top:-.8em;background:#f5f5f5;height:1.5em;width:1.5em;border:.1em solid rgba(0,0,0,.05);text-align:center;font:italic 700 1em/1.5em Georgia,Serif;color:#ccc;-moz-border-radius:1.5em;-webkit-border-radius:1.5em;border-radius:1.5em;-webkit-transition:all .2s ease-out;-moz-transition:all .2s ease-out;-ms-transition:all .2s ease-out;-o-transition:all .2s ease-out;transition:all .2s ease-out}.circle-list li:hover h2:before{background-color:#ffd797;border-color:rgba(0,0,0,.08);border-width:.2em;color:#444;-webkit-transform:scale(1.5);-moz-transform:scale(1.5);-ms-transform:scale(1.5);-o-transform:scale(1.5);transform:scale(1.5)}.fa{padding:20px;font-size:30px;width:30px;text-align:center;margin:5px 2px;border-radius:50%}.fa:hover{opacity:.7}.fa-github{background:#000;color:#fff}.fa-facebook{background:#3B5998;color:#fff}.fa-twitter{background:#55ACEE;color:#fff}.fa-google{background:#dd4b39;color:#fff}.fa-linkedin{background:#007bb5;color:#fff}.fa-youtube{background:#b00;color:#fff}.fa-instagram{background:#125688;color:#fff}.fa-pinterest{background:#cb2027;color:#fff}.fa-snapchat-ghost{background:#fffc00;color:#fff;text-shadow:-1px 0 #000,0 1px #000,1px 0 #000,0 -1px #000}.fa-skype{background:#00aff0;color:#fff}.fa-android{background:#a4c639;color:#fff}.fa-dribbble{background:#ea4c89;color:#fff}.fa-vimeo{background:#45bbff;color:#fff}.fa-tumblr{background:#2c4762;color:#fff}.fa-vine{background:#00b489;color:#fff}.fa-foursquare{background:#45bbff;color:#fff}.fa-stumbleupon{background:#eb4924;color:#fff}.fa-flickr{background:#f40083;color:#fff}.fa-yahoo{background:#430297;color:#fff}.fa-soundcloud{background:#f50;color:#fff}.fa-reddit{background:#ff5700;color:#fff}.fa-rss{background:#f60;color:#fff}</style></head><body> <h1>Ebay\'s scrapping category</h1> <h3>Author: Felix E. Orduz G. - <a href="mailto:felix.orduz@gmail.com">felix.orduz@gmail.com</a></h3>' 
html_template_footer = '<div style="text-align: center"> <a href="https://github.com/axidsugar" class="fa fa-github"></a> <a href="https://www.facebook.com/axidsugar" class="fa fa-facebook"></a> <a href="https://twitter.com/axidsugar" class="fa fa-twitter"></a> <a href="https://www.youtube.com/user/axidsugar" class="fa fa-youtube"></a> <a href="https://www.instagram.com/axidsugar/" class="fa fa-instagram"></a> </div></body></html>' 
sql_create_category_table = """ CREATE TABLE IF NOT EXISTS category (category_id integer PRIMARY KEY,category_name text NOT NULL,category_level integer,parent_id integer,best_offer_enabled boolean);"""
#Header for ebay's API
headers = {'X-EBAY-API-CALL-NAME': 'GetCategories','X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841','X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db','X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19','X-EBAY-API-SITEID': '0','X-EBAY-API-COMPATIBILITY-LEVEL': '861'}
#Content to get categories from ebay's API
data = '<?xml version="1.0" encoding="utf-8"?><GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents"><RequesterCredentials><eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PlLuWA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GlDpaDpAudj6x9nY+seQ**LyoEAA**AAMAAA**wSd/jBCbxJHbYuIfP4ESyC0mHG2Tn4O3v6rO2zmnoVSF614aVDFfLSCkJ5b9wg9nD7rkDzQayiqvwdWeoJkqEpNQx6wjbVQ1pjiIaWdrYRq+dXxxGHlyVd+LqL1oPp/T9PxgaVAuxFXlVMh6wSyoAMRySI6QUzalepa82jSQ/qDaurz40/EIhu6+sizj0mCgjcdamKhp1Jk3Hqmv8FXFnXouQ9Vr0Qt+D1POIFbfEg9ykH1/I2CYkZBMIG+k6Pf00/UujbQdne6HUAu6CSj9wGsqQSAEPIXXvEnVmtU+6U991ZUhPuA/DMFEfVlibvNLBA7Shslp2oTy2T0wlpJN+f/Jle3gurHLIPc6EkEmckEpmSpFEyuBKz+ix4Cf4wYbcUk/Gr3kGdSi20XQGu/ZnJ7Clz4vVak9iJjN99j8lwA2zKW+CBRuHBjZdaUiDctSaADHwfz/x+09bIU9icgpzuOuKooMM5STbt+yJlJZdE3SRZHwilC4dToTQeVhAXA4tFZcDrZFzBmJsoRsJYrCdkJBPeGBub+fqomQYyKt1J0LAQ5Y0FQxLHBIp0cRZTPAuL/MNxQ/UXcxQTXjoCSdZd7B55f0UapU3EsqetEFvIMPxCPJ63YahVprODDva9Kz/Htm3piKyWzuCXfeu3siJvHuOVyx7Q4wyHrIyiJDNz5b9ABAKKauxDP32uqD7jqDzsVLH11/imKLLdl0U5PN+FP30XAQGBAFkHf+pAvOFLrdDTSjT3oQhFRzRPzLWkFg</eBayAuthToken></RequesterCredentials><CategorySiteID>0</CategorySiteID><DetailLevel>ReturnAll</DetailLevel></GetCategoriesRequest>'
#Ebay's sdk url
ebay_sdk_url='https://api.sandbox.ebay.com/ws/api.dll'
#this method creates a new connection to sqlite
xmlns='{urn:ebay:apis:eBLBaseComponents}'
#Database
database='database.db'

#Function to create a new database connection
def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
 
	return None

#this method executes a sql sentence
def execute_sql(conn,sql,data):
	try:
		c = conn.cursor()
		if data is None:
			c.execute(sql)
		else:
			c.execute(sql, data)
		conn.commit()
	except Error as e:
		print(e)

#Function re-builds database from Ebay's API
def re_build():
	#new Database connection
	conn = create_connection(database)
	
	#Sentence to create or purge category table
	execute_sql(conn, sql_create_category_table,None)
	sql_truncate_category_table =""" DELETE FROM category;"""
	execute_sql(conn, sql_truncate_category_table,None)
	execute_sql(conn, """VACUUM;""",None)

	#Request
	r = requests.post(ebay_sdk_url,data,headers=headers)

	#Convert response text to XML
	root = ET.fromstring(r.text)

	#Loop to insert categories
	CategoryArray = root.find(xmlns+'CategoryArray');
	for child in CategoryArray:
		
		category_id = child.find(xmlns+'CategoryID')
		if category_id is not None:
			category_id = category_id.text

		category_name = child.find(xmlns+'CategoryName')
		if category_name is not None:
			category_name = category_name.text

		category_level = child.find(xmlns+'CategoryLevel')
		if category_level is not None:
			category_level = category_level.text

		parent_id = child.find(xmlns+'CategoryParentID')
		if parent_id is not None:
			parent_id = parent_id.text

		best_offer_enabled = child.find(xmlns+'BestOfferEnabled')
		if best_offer_enabled is not None:
			best_offer_enabled =best_offer_enabled.text
		
		values = (category_id, category_name, category_level,parent_id, best_offer_enabled)

		sql_insert_category = """INSERT INTO category (category_id,category_name,category_level,parent_id,best_offer_enabled) VALUES (?,?,?,?,?)"""

		execute_sql(conn, sql_insert_category, values)				

	conn.close()

#Funtion to get all categories by id 
def render_cat(category):
	#new Database connection
	conn = create_connection(database)

	sql_query_category = 'SELECT cat.category_id id, cat.category_name name, cat.category_level level, cat.parent_id parent, cat.best_offer_enabled best_offer, sub.category_id, sub.category_name, sub.category_level, sub.parent_id, sub.best_offer_enabled FROM category AS cat LEFT OUTER JOIN category AS sub ON cat.category_id = sub.parent_id WHERE cat.category_id = ?  ORDER BY sub.category_level ASC;'

	t=(category,)
	text = '<ul class="rounded-list"><li>'
	i=0;
	fg = 0
	for row in conn.execute(sql_query_category,t):	
		text = text 
		if fg==0 and row[5] is not None and row[0] != row[5]:
			text = text + '<a href="#">' + str(row[0]) +' - ' + row[1]+' - ' + str(row[2])+' - ' + str(row[4]) + '</a>'+render_cat(row[5])
			fg = 1;
		elif fg!=0 and row[5] is not None and row[0] != row[5]:
			text = text + render_cat(row[5])
		elif row[5] is None:
			text = text + '<a href="#">' + str(row[0]) +' - ' + row[1]+' - ' + str(row[2])+' - ' + str(row[4]) + '</a>'
		i = i+1
	
	text = text + '</li></ul>'

	if i==0:
		return None
	return text

#render categories in HTML
def render_html(render):

	html = render_cat(render)
	if html is not None:
		with open(render+".html", "w") as file:
			file.write(str(html_template_header)+str(html)+str(html_template_footer))
	else:
		print ('No category with ID: '+str(render))

#Main function
def main(rebuild,render):
	header_html = ''
	if rebuild:
		re_build()
	elif render:
		render_html(render)
		
#Params
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Scrapping Ebay Categories')
	parser.add_argument("-r","--rebuild", help="Get categories from ebay",action="store_true" )
	parser.add_argument("-e","--render", help="Render category" )
	args = parser.parse_args()
	main(args.rebuild,args.render)