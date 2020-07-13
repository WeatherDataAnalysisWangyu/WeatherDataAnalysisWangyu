package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

//拉起选择城市、日期，预测天气的界面
@Controller
public class PredictController {

    @RequestMapping("/predict")
    public String home() {
        return "predict";
    }
}