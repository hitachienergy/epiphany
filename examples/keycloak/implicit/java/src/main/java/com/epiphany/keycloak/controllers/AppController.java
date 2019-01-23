package com.epiphany.keycloak.controllers;
 
import java.security.Principal;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.ServletException;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import com.epiphany.keycloak.models.AppConfig;
import org.springframework.web.servlet.view.RedirectView;
import org.keycloak.adapters.springsecurity.token.KeycloakAuthenticationToken;
import org.keycloak.KeycloakPrincipal;
import org.keycloak.KeycloakSecurityContext;
import org.keycloak.representations.AccessToken;
import java.util.Map;
import java.lang.*;
 
@Controller
public class AppController {
    @RequestMapping(value = "/config", method = RequestMethod.GET)
    @ResponseBody
    public ResponseEntity<AppConfig> config(HttpServletRequest request) {
        Map<String, String> env = System.getenv();
        return ResponseEntity.ok(new AppConfig(env.get("realm"), env.get("url"), env.get("clientid")));
    }     
}