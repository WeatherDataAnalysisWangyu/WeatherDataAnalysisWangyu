package com.example.demo.controller;

//import com.mysql.*;

import java.sql.*;

public class sql {
	private static Connection getConn() {

		String driver = "com.mysql.cj.jdbc.Driver";
		String url = "jdbc:mysql://127.0.0.1:3306/weather?allowPublicKeyRetrieval=true&serverTimezone=UTC";
		String username = "root";
		String password = "123";
		Connection conn = null;
		try {
			Class.forName(driver);
			conn = DriverManager.getConnection(url, username, password);
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return conn;
	}

	public int insert(user student) {
		Connection conn = getConn();
		int i = 0;
		String ins = "insert into `temp` (`name`, `password`) values (?, ?)";
		PreparedStatement insertstatement;
		try {
			insertstatement = conn.prepareStatement(ins);

			insertstatement.setString(1, student.getName());
			insertstatement.setString(2, student.getPassword());

			i = insertstatement.executeUpdate();

			insertstatement.close();
			conn.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return i;
	}

	public int delete(String name) {
		Connection conn = getConn();
		int i = 0;
		String sql = "delete from temp where name='" + name + "'";
		PreparedStatement deletestatement;
		try {
			deletestatement = conn.prepareStatement(sql);
			i = deletestatement.executeUpdate();
			System.out.println("result: " + i);
			deletestatement.close();
			conn.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return i;
	}

	public boolean selectName(user student) throws SQLException {
		Connection con = getConn();
		try{
			String sel = "select Name from temp where Name = ?";
			PreparedStatement selectstatement = con.prepareStatement(sel);
			selectstatement.setString(1, student.getName());
			ResultSet rs = selectstatement.executeQuery();
			rs.next();
			int count = rs.getInt(1);
			if(count > 0){
				return true;
			}
		}catch(Exception e){
			e.printStackTrace();
		}
			return false;
		}

	public boolean selectPassword(user student) throws SQLException {
		Connection con = getConn();
		try{
			String sel = "select Password from temp where Password = ?";
			PreparedStatement selectstatement = con.prepareStatement(sel);
			selectstatement.setString(1, student.getPassword());
			ResultSet rs = selectstatement.executeQuery();
			rs.next();
			int count = rs.getInt(1);
			if(count > 0){
				return true;
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		return false;
	}

}