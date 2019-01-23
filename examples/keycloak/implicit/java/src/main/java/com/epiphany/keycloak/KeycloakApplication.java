package com.epiphany.keycloak;

import java.util.Properties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerResponse;
import org.springframework.web.reactive.function.server.RouterFunctions;
import static org.springframework.web.reactive.function.server.RequestPredicates.GET;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import static org.springframework.web.reactive.function.server.ServerResponse.ok;
import static org.springframework.http.MediaType.TEXT_HTML;

@SpringBootApplication
public class KeycloakApplication {
	public static void main(String[] args) {
                SpringApplication app = new SpringApplication(KeycloakApplication.class);
                Properties properties = new Properties();
                properties.setProperty("spring.resources.static-locations", "classpath:/wwwroot/");
                app.setDefaultProperties(properties);
                app.run(args);
	}
}
 

