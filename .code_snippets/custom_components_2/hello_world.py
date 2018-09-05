
import logging

_LOGGER = logging.getLogger(__name__)

# The domain of your component. Equal to the filename of your component.
DOMAIN = "hello_world"


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    """Setup the hello_world component."""
	
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.set('hello_world.Hello_Wonderful_World', 'This Works!')

	
	
	
    count = 0	
	
    # Listener to handle fired events
    def handle_event(event):
        nonlocal count
        count += 1
        print('Total events received:', count)
        answer = event.data.get('answer', '0')
        _LOGGER.info(answer)
        hass.states.set('hello_world.Answer', answer)



    # Listen for when my_cool_event is fired
    hass.bus.listen('my_cool_event', handle_event)
	

	
	
	# Fire event my_cool_event with event data answer=42
    hass.bus.fire('my_cool_event', { 'answer': 42 })
	
	# Fire event my_cool_event with event data answer=43
    hass.bus.fire('my_cool_event', { 'answer': 43 })

	# Fire event my_cool_event with event data answer=44
    hass.bus.fire('my_cool_event', { 'answer': 44 })
	
	
	
    # Return boolean to indicate that initialization was successfully.
    return True
	
	