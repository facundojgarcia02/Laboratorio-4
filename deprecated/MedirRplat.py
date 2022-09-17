from utils.experiments.examples.ferromagnetism import Ferromagnetism
from utils.misc import save_df

ferro = Ferromagnetism(PLOT = True)

df = ferro.inf_measure()
#save_df(df)