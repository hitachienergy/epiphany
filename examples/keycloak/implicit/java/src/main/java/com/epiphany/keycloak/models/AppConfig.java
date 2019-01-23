package com.epiphany.keycloak.models;

import java.io.Serializable;

public class AppConfig implements Serializable {
	String realm;
	String url;
	String clientId;
    
	public AppConfig(String realm, String url, String clientId) {
		this.realm = realm;
		this.url = url;
		this.clientId = clientId;
    }	
    
	public String getRealm() {
		return realm;
    }
    
	public void setRealm(String realm) {
		this.realm = realm;
    }
    
	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	} 
	
	public String getClientId() {
		return clientId;
	}
	
	public void setClientId(String clientId) {
		this.clientId = clientId;
	}  	
}