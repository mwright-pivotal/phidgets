package demo.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class PhidgetController {
	@Autowired JdbcTemplate jdbcTemplate;
	
	@RequestMapping("/spatial")
	public String listSpatial() {
		return "spatial/list";
	}
	
	@RequestMapping("/")
	public String home() {
		return "spatial/line";
	}
	
	@RequestMapping("/spatialGraph")
	public String lineSpatial() {
		return "spatial/line";
	}
}
