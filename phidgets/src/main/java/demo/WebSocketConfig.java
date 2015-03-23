package demo;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.converter.MessageConverter;
import org.springframework.messaging.simp.config.ChannelRegistration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.messaging.simp.config.StompBrokerRelayRegistration;
import org.springframework.web.socket.config.annotation.AbstractWebSocketMessageBrokerConfigurer;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.util.List;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig extends AbstractWebSocketMessageBrokerConfigurer {
	JsonNode vcapServices;
	@Override
	public void configureMessageBroker(MessageBrokerRegistry config) {
		StompBrokerRelayRegistration relay = config.enableStompBrokerRelay("/topic/").setRelayHost(getRabbitUri());
		relay.setSystemLogin(this.getRabbitUsername());
		relay.setSystemPasscode(this.getRabbitPswd());
		relay.setClientLogin(this.getRabbitUsername());
		relay.setClientPasscode(this.getRabbitPswd());
		relay.setVirtualHost(this.getRabbitVhost());
	}

	@Override
	public void registerStompEndpoints(StompEndpointRegistry registry) {
		registry.addEndpoint("/phidget-ws").withSockJS();
	}
	
	private JsonNode getVcapServices() {
		if (vcapServices!=null)
			return vcapServices;
		String vcap_services = System.getenv("VCAP_SERVICES");
		if (vcap_services==null)
			return null;
		JsonFactory factory = new JsonFactory();
		try {
			ObjectMapper mapper = new ObjectMapper();
			vcapServices = mapper.readTree(vcap_services);
		} catch (JsonParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return vcapServices;
	}
	
	private String getRabbitUri() {
		if (this.getVcapServices()==null)
			return "10.20.0.46";
		JsonNode rabbitMqNode = this.getVcapServices().get("p-rabbitmq");
		JsonNode credentials = rabbitMqNode.get(0).get("credentials");
		return credentials.get("protocols").get("stomp").get("host").textValue();
	}
	
	private String getRabbitUsername() {
		if (this.getVcapServices()==null)
			return "admin";
		JsonNode rabbitMqNode = this.getVcapServices().get("p-rabbitmq");
		JsonNode credentials = rabbitMqNode.get(0).get("credentials");
		return credentials.get("username").textValue();
	}
	
	private String getRabbitPswd() {
		if (this.getVcapServices()==null)
			return "admin";
		JsonNode rabbitMqNode = this.getVcapServices().get("p-rabbitmq");
		JsonNode credentials = rabbitMqNode.get(0).get("credentials");
		return credentials.get("password").textValue();
	}
	
	private String getRabbitVhost() {
		if (this.getVcapServices()==null)
			return "admin";
		JsonNode rabbitMqNode = this.getVcapServices().get("p-rabbitmq");
		JsonNode credentials = rabbitMqNode.get(0).get("credentials");
		return credentials.get("vhost").textValue();
	}
}