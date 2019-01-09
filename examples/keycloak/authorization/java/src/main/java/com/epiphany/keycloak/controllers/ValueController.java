package com.epiphany.keycloak.controllers;

import java.util.List;
import java.util.ArrayList;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PathVariable;
import com.epiphany.keycloak.models.Value;

@RestController
@RequestMapping("/api/Values")
class ValueController {
    static final List<Value> data = new ArrayList<Value>() {{
        add(new Value(1, "1"));
        add(new Value(2, "2"));
        add(new Value(3, "3"));
    }};

	@GetMapping
    public ResponseEntity<List<Value>> getAllValues() {
        return ResponseEntity.ok(data);
    }
 
	@GetMapping("/{id}")
    public ResponseEntity<Value> getValueById(@PathVariable(value = "id") int valueId) {
        return ResponseEntity.ok(new Value(valueId, Integer.toString(valueId)));
    }
}