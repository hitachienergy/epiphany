package com.epiphany.keycloak.models;

import java.io.Serializable;

public class Value implements Serializable {
	int id;
    String value;
    
	public Value(int id, String value) {
		this.id = id;
		this.value = value;
    }	
    
	public int getId() {
		return id;
    }
    
	public void setId(int id) {
		this.id = id;
    }
    
	public String getValue() {
		return value;
	}
	public void setValue(String value) {
		this.value = value;
	}    
}