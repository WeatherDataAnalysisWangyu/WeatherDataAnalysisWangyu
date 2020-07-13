package com.example.demo.controller;

public class user {
	private String name;
	private String password;
	user(String string, String string2){
		this.name=string;
		this.password=string2;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
}
