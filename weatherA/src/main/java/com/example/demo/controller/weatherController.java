package com.example.demo.controller;

import java.io.*;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;

//获取选择的城市、日期，从而生成arima的json文件
@Controller
public class weatherController {

	String city, month, day;

	public String getCity() {
		return this.city;
	}

	public void setCity(String loginId) {
		this.city = loginId;
	}

	public String getMonth() {
		return this.month;
	}

	public void setMonth(String loginId) {
		this.month = loginId;
	}

	public String getDay() {
		return this.day;
	}

	public void setDay(String loginId) {
		this.day = loginId;
	}


	@RequestMapping("/targetAdd")
    public void targetAdd(@RequestBody submitController sub, HttpServletResponse response)
                            		throws IOException, InterruptedException{
		setCity(sub.city);
		setMonth(sub.month);
		setDay(sub.day);


		String[] str = new String[2];
		System.out.println(city);
		System.out.println(month);
		System.out.println(day);
		String[] args = new String[] { "python", "D:\\weatherDataAnalysis\\test.py", city, month, day };
	    Process proc = Runtime.getRuntime().exec(args);// 执行py文件
//	    BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
		System.out.println("success");
		proc.waitFor();


    }

}
