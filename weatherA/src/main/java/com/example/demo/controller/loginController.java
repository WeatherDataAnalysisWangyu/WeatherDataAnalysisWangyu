package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;

import java.util.Map;

//拉起登录的初始界面
@Controller
public class loginController {


    @RequestMapping("/login")
    public String home(){
        return "loginzwh";
    }

//    public String targetAdd(@RequestParam(value = "userName",required = false) String userName,
//                            @RequestParam(value = "password",required = false) String password){
//
//
//        System.out.println("cityName is:"+userName);
//
//        System.out.println("searchDate is:"+password);
//
//        return "successful";
//
//    }


}
