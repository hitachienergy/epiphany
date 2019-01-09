package com.epiphany.keycloak.controllers;
 
import java.security.Principal;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.ServletException;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.view.RedirectView;
import org.keycloak.adapters.springsecurity.token.KeycloakAuthenticationToken;
import org.keycloak.KeycloakPrincipal;
import org.keycloak.KeycloakSecurityContext;
import org.keycloak.representations.AccessToken;
 
@Controller
public class AppController {
    @RequestMapping(value = "/state", method = RequestMethod.GET)
    @ResponseBody
    public String state(HttpServletRequest request) {
        Principal principal = request.getUserPrincipal();
        if (principal == null) {
            return "{\"authenticated\": false}";
        } else {
            return "{\"authenticated\": true}";
        }
    }

    @RequestMapping(value = "/login", method = RequestMethod.GET)
    @ResponseBody
    public RedirectView login(HttpServletRequest request) {
        return new RedirectView("/");
    }   

    @RequestMapping(value = "/token", method = RequestMethod.GET)
    @ResponseBody
    public String token(HttpServletRequest request) {
        KeycloakAuthenticationToken token = (KeycloakAuthenticationToken) request.getUserPrincipal();        
        KeycloakPrincipal principal = (KeycloakPrincipal)token.getPrincipal();
        KeycloakSecurityContext session = principal.getKeycloakSecurityContext();
        return "{\"token\": \"" + session.getTokenString() + "\"}";
    }    
    
    @RequestMapping(value = "/logout", method = RequestMethod.GET)
    @ResponseBody
    public RedirectView logout(HttpServletRequest request) {
        try {
            request.logout();
        }
        catch( Exception ex){

        }        
        return new RedirectView("/");
    }     
}