package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.awt.*;
import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;

//获得登陆界面的用户名与密码
@Controller
public class searchController {

    String username,password;

    public String getUserName() {
        return this.username;
    }

    public void setUserName(String loginId) {
        this.username = loginId;
    }

    public String getPassword() {
        return this.password;
    }

    public void setPassword(String loginId) {
        this.password = loginId;
    }


    @RequestMapping(value = "/canilogin")
    public String search(@RequestParam("password") String password, @RequestParam("account") String username, Model model) throws SQLException {
        setUserName(username);
        setPassword(password);

        System.out.println(getUserName());
        System.out.println(getPassword());

        sql s = new sql();
        if(!s.selectName(new user(username, password))) {
            model.addAttribute("msg", "用户名不存在！");
//            return "loginzwh";
        }
        else if(!s.selectPassword(new user(username, password))) {
            model.addAttribute("msg", "密码错误！");
//            return "loginzwh";
        }
        else{
            return "predict";
        }
        return "loginzwh";

    }



}
