package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.awt.*;
import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;

//获取注册界面的用户名、密码与邮箱
@Controller
public class adduserController {

    String username,password,password2;

    public String getUsername() {
        return this.username;
    }

    public void setUsername(String loginId) {
        this.username = loginId;
    }

    public String getPassword() {
        return this.password;
    }

    public void setPassword(String loginId) {
        this.password = loginId;
    }

    public String getPassword2() {
        return this.password2;
    }

    public void setPassword2(String loginId) {
        this.password2 = loginId;
    }

    @RequestMapping(value = "/leileleile")
    public String search(@RequestParam("name")String username, @RequestParam("Password") String password1, @RequestParam("mainPassword") String password2, Model model) throws SQLException {
        setUsername(username);
        setPassword(password1);
        setPassword2(password2);

        System.out.println(getUsername());
        System.out.println(getPassword());
        System.out.println(getPassword2());

        sql s = new sql();
        if(s.selectName(new user(username, password1))) {
            model.addAttribute("msg", "用户名已存在！");
        }
        else if(!password1.equals(password2)){
            model.addAttribute("msg1", "两次密码不一致！");
        }
        else{
            s.insert(new user(username, password1));
            return "loginzwh";
        }

       return "registerzwh";

    }



//    @ModelAttribute
//    @RequestMapping(value = "/leileleile")
//    public String search(@RequestBody adduserController sub, HttpServletResponse response, Model model) throws SQLException {
//
//        setUsername(sub.username);
//        setPassword(sub.password);
//        setPassword2(sub.password2);
//
////        return "loginzwh";
//        sql s = new sql();
//        if(s.selectName(new user(username, password))) {
//            System.out.println("10000000000000000000");
//            model.addAttribute("msg", "用户名已存在！");
//            return "/registerzwh.html";
//        }
//        else if(!password.equals(password2)){
//            System.out.println("2000000000000000000");
//            model.addAttribute("msg1", "两次密码不一致！");
//            return "/registerzwh.html";
//        }
//        else{
//            System.out.println("3000000000000000000");
//            return "/loginzwh.html";
//        }

//        System.out.println(getUsername());
//        System.out.println(getPassword());
//        System.out.println(getPassword2());

//        return "registerzwh";
//    }



}