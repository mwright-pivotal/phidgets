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
		relay.setSystemLogin("6475c30d-e658-4e75-aa13-83cfb384b53d");
		relay.setSystemPasscode("gh6l264kcer94qf5ic2bcrj9tl");
		relay.setClientLogin("6475c30d-e658-4e75-aa13-83cfb384b53d");
		relay.setClientPasscode("gh6l264kcer94qf5ic2bcrj9tl");
		relay.setVirtualHost("b2a4c452-ef36-4320-8bf4-8bfb242e3277");
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
}