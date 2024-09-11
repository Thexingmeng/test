package org.example.helloworld;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
//基本的接口类，没什么好说的
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello World";
    }
}
