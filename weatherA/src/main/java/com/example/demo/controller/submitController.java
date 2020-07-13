package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.awt.*;
import java.io.IOException;
import java.util.HashMap;

@Controller
public class submitController {

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

    @RequestMapping(value = "/search555")
    public void search(@RequestBody submitController sub, HttpServletResponse response){
        setCity(sub.city);
        setMonth(sub.month);
        setDay(sub.day);

        System.out.println(getCity());
        System.out.println(getMonth());
        System.out.println(getDay());
    }



}
