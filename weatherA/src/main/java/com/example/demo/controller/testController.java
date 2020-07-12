package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Controller
public class testController {

    @RequestMapping("/test")
    public String home() {

        return "test";
    }

}