from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        consumo_medio_mensile = []

        for impianto in self._impianti:
            lista_consumi = impianto.get_consumi()
            lista_consumi_mese = []
            giorni_di_consumo = set()

            for consumo in lista_consumi:
                if consumo.data.month == mese:
                    giorni_di_consumo.add(consumo.data.day)
                    lista_consumi_mese.append(consumo.kwh)

            media = 0.0
            if lista_consumi_mese :
                somma_kwh = sum(lista_consumi_mese)
                numero_giorni = len(giorni_di_consumo)
                if numero_giorni > 0:
                    media = somma_kwh / numero_giorni

            consumo_medio_mensile.append((impianto.nome, media))

        return consumo_medio_mensile



    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO

        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale[:]
            return

        if self.__costo_ottimo != -1 and costo_corrente >= self.__costo_ottimo:
            return

        for impianto in self._impianti:
            impianto_id = impianto.id

            costo_spostamento = 0 #sussiste solo se l'impianto è cambiato e se non è il giorno 1.

            if ultimo_impianto is not None and ultimo_impianto != impianto_id:
                costo_spostamento = 5

            costo_variabile = consumi_settimana.get(impianto_id, {}).get(giorno, 0)
            costo_giornaliero = costo_spostamento + costo_variabile

            nuova_sequenza = sequenza_parziale + [impianto_id]
            nuovo_costo = costo_giornaliero + costo_corrente

            self.__ricorsione(
                nuova_sequenza,
                giorno + 1,
                impianto_id,
                nuovo_costo,
                consumi_settimana
            )

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO

        consumi_settimana = {}
        for impianto in self._impianti:
            consumi_giornalieri = {}

            lista_consumi = impianto.get_consumi()

            for consumo in lista_consumi:
                if consumo.data.month == mese and 1 <= consumo.data.day <= 7:
                    giorno = consumo.data.day

                    if giorno in consumi_giornalieri:
                        consumi_giornalieri[giorno] += consumo.kwh
                    else:
                        consumi_giornalieri[giorno] = consumo.kwh

            consumi_settimana[impianto.id] = consumi_giornalieri

        return consumi_settimana




