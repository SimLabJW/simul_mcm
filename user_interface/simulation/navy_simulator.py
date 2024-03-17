import logging
from simulation.navy_manager import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class start_simulator():

    def start() -> None:
        print("Start simulator")
        start_simulation_manager = Navy_manager().start()

# start_simulator.start()