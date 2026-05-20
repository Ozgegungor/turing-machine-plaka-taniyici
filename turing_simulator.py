import string

class TuringMachine:
    def __init__(self, tape_input):
        self.tape = list(tape_input) + ['_']
        self.head_position = 0
        self.current_state = 'q0'
        self.accept_state = 'q7'
        self.reject_state = 'q_reject'
        
        self.digits = set(string.digits)  # 0-9
        self.uppercase = set(string.ascii_uppercase) # A-Z
        
        # Yapı: (mevcut_durum, karakter_tipi) -> (sonraki_durum)
        self.transitions = {
            ('q0', 'rakam'): 'q1',
            ('q1', 'rakam'): 'q2',
            ('q2', 'harf'): 'q3',
            ('q3', 'harf'): 'q4',
            ('q4', 'rakam'): 'q5',
            ('q5', 'rakam'): 'q6',
            ('q6', 'rakam'): 'q7',
            ('q7', 'blank(boşluk)'): 'q7' # Kabul durumu, başarılı bitiş
        }

    def _get_char_type(self, char):
        if char in self.digits:
            return 'rakam'
        elif char in self.uppercase:
            return 'harf'
        elif char == '_':
            return 'blank(boşluk)'
        else:
            return 'geçersiz' # Küçük harfler veya özel karakterler için

    def print_step(self, step_num, read_char, action):
        # Kafanın nerede olduğunu göstermek için bandın altına bir ok işareti koyuyoruz
        tape_str = " ".join(self.tape)
        pointer_str = " " * (self.head_position * 2) + "^"
        
        print(f"\n--- Adım {step_num} ---")
        print(f"Mevcut Durum : {self.current_state}")
        print(f"Okunan Sembol: '{read_char}'")
        print(f"Kafa Hareketi: {action}")
        print(f"Bant İçeriği : {tape_str}")
        print(f"Kafa Konumu  : {pointer_str}")

    def run(self):
        print(f"Girdi Bandı: {''.join(self.tape[:-1])}")
        step = 1
        
        while self.current_state not in [self.reject_state]:
            # Bant sınırları dışına çıkma kontrolü
            if self.head_position < 0 or self.head_position >= len(self.tape):
                self.current_state = self.reject_state
                break
                
            read_char = self.tape[self.head_position]
            char_type = self._get_char_type(read_char)

            lookup_key = (self.current_state, char_type)
            
            if lookup_key in self.transitions:
                next_state = self.transitions[lookup_key]
                
                # Eğer q7 durumundaysak ve blank(boşluk) okuduysak işlem başarıyla tamamlanmıştır
                if self.current_state == 'q7' and char_type == 'blank(boşluk)':
                    action = "STAY (Durdu)"
                    self.print_step(step, read_char, action)
                    break
                else:
                    action = "RIGHT (Sağa)"
                    self.print_step(step, read_char, action)
                    self.current_state = next_state
                    self.head_position += 1
            else:
                # Eşleşen kural yoksa doğrudan RED durumuna geç
                action = "STAY (Hatalı Karakter/Format)"
                self.current_state = self.reject_state
                self.print_step(step, read_char, action)
                break
                
            step += 1

        # Sonuç
        if self.current_state == self.accept_state:
            print("SONUÇ: KABUL")
            return "KABUL"
        else:
            print("SONUÇ: RED")
            return "RED"
        
if __name__ == "__main__":
    kullanici_girdisi = input("Lütfen kontrol edilecek plaka bilgisini giriniz: ")
    
    # Girilen boşlukları temizler ve başlatır
    plaka = kullanici_girdisi.strip()
    
    tm = TuringMachine(plaka)
    tm.run()
