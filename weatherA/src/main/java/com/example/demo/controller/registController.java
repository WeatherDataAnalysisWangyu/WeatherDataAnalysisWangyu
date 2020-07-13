package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

//拉起注册的界面
@Controller
public class registController {

    @RequestMapping("/register")
    public String home() {
        return "registerzwh";
    }
}
