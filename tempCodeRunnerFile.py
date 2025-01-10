import json
from datetime import datetime

import os

file_path = 'data_pemebelian.json'
if os.path.exists(file_path):
    print("File dapat diakses.")
else:
    print("File tidak ada.")
class Node: #mempresentasikan satu item menu dengan harga
    def __init__(self, item, harga):
        self.item = item
        self.harga = harga
        self.next = None

class Node_Pemesanan:   #menyimpan pesanan
    def __init__(self, nama, item, total_harga):
        self.nama = nama
        self.item_pemesanan = item
        self.total_harga = total_harga
        self.next = None

class LinkedList:       #menyimpan item menu
    def __init__(self):
        self.head = None

    def __iadd__(self, data):
        item, harga = data
        new_node = Node(item, harga)
        if not self.head:
            self.head = new_node
        else:
            last_node = self.head
            while last_node.next:
                last_node = last_node.next
            last_node.next = new_node
        return self 
            
    def display(self):
        current = self.head
        if not current:
            print("Tidak ada pesanan")
            return
        while current:
            print(f"{current.item:<15} - Rp{current.harga:<10}")
            current = current.next
        print("") 
    
    def bubble_sort(self, by='item'):
        if not self.head or not self.head.next:         #mengecek kondisi linkedlist dan mulai sort
            return
        swapped = True          
        
        while swapped:      #memastikan penyususran linkedlist dilakukan selama masih ada elemen yang perlu ditukar        
            swapped = False
            current = self.head
            while current.next:
                if  (by == 'item' and current.item > current.next.item) or \
                    (by == 'harga' and current.harga > current.next.harga):

                    current.item, current.next.item = current.next.item, current.item           #menukar elemen jika tidak dalam urutan yang benar
                    current.harga, current.next.harga = current.next.harga, current.harga
                    swapped = True
                current = current.next          #traversal ke node berikutnya
                    

item_list = LinkedList()            #daftar item dan harga
item_list += ("kopi", 3000)
item_list += ("es teh", 4000)
item_list += ("roti aoka", 2500)
item_list += ("le mineral", 5000)
item_list += ("nasgor", 10000)
item_list += ("krupuk", 1000)
item_list += ("susu", 6000)
item_list += ("bakwan", 1000)
item_list += ("ayam geprek", 8000)

class Queue:            #membuat dan mengelola antrian pemesanan 
    def __init__(self, json_file='data_pemebelian.json'):
        self.head = None
        self.tail = None
        self.json_file = json_file
        self.total_pembelian = 0
        self.load_json()

    def enqeue(self, nama, item, total_harga):    #menambahkan pemesanan ke antrian
        add_item = Node_Pemesanan(nama, item, total_harga) 
        if not self.head:
            self.head = add_item
            self.tail = add_item
        else:
            self.tail.next = add_item
            self.tail = add_item
            
        self.save_json(add_item)
        
    def display_queue(self):            #menampilkan daftar antrian
        current = self.head
        if not current:
            print("tidak ada pesanan")
            return
        while current:
            print(f"Nama: {current.nama}, total harga: Rp {current.total_harga}")
            current.item_pemesanan.display()
            current = current.next
    
    def save_json(self, pemesanan):         #menyimpan pesanan ke file json
            pemesanan_data = {
            'nama':pemesanan.nama,
            'item_pemesanan':[],
            'total_harga':pemesanan.total_harga,
            'tanggal':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            current = pemesanan.item_pemesanan.head
            while current:
                pemesanan_data['item_pemesanan'].append({
                    "item" : current.item,
                    "harga" : current.harga
                })
                current = current.next

            try:
                try:
                    with open(self.json_file, "r") as file:
                        content = file.read().strip()
                        if not content:
                            existing_data = []
                        else:
                            existing_data = json.loads(content)
                except FileNotFoundError:
                    existing_data = []

                existing_data.append(pemesanan_data)

                with open(self.json_file, "w") as file:
                    json.dump(existing_data, file, indent=4)
                
            except Exception as e:
                print("eror menyimpan", e)

    def load_json(self):            #membuat data pemesanan file json ke antrian        
        try:
            with open(self.json_file, "r") as file:
                content = file.read().strip()
                if not content:
                     print("No previous data found, starting fresh.")
                     return
                orders = json.loads(content)  # Memuat langsung dari file
                for pemesanan in orders:
                    item_list = LinkedList()
                    for item in pemesanan["item_pemesanan"]:
                        item_list += (item["item"], item["harga"])
                add_item = Node_Pemesanan(pemesanan["nama"], item_list, pemesanan["total_harga"])
                if not self.head:
                    self.head = add_item
                    self.tail = add_item
                else:
                    self.tail.next = add_item
                    self.tail = add_item
                   
        except FileNotFoundError:
            print("No previous data found, starting fresh.")
        except json.JSONDecodeError:
            print("Error loading JSON file: file tidak valid.")                
    
class Stack:
    def __init__(self):
            self.top = None

    def push(self, data):
        new_node = Node(data, None)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.is_empty():
            print("stack kosong, tidak ada yang bisa dihapus")
            return None
        pooped_node = self.top
        self.top = self.top.next
        return pooped_node

    def is_empty(self):
        return self.top is None

    def display(self):
        current = self.top
        if not current:
            print("stak kosong")
            return
        print("isi stak: ")
        while current:
            print(current.item)
            current = current.next
        print('')

def print_daftar_harga(item_list):          #menampilkan item menu dan harga
    print("       DAFTAR ITEM       ")
    item_list.display()

    
def find_item_price(items, item_name):      # mencari nama item
    current = items.head
    while current:
        if current.item.lower() == item_name.lower():
            return current.harga
        current = current.next
    return None  #jika item tidak ditemukan

def calculate_total(queue, stack):         #menghitung total pesanan
    total = 0
    pesanan = LinkedList()
    nama_pembeli = input("masukkan nama pembeli: ")
    print("\nMasukkan pesanan Anda (ketik 'stop' untuk selesai):")
    
    while True:
        item_name = input("Nama item: ")
        if item_name.lower() == "stop":
            break
        # Cari harga item
        harga = find_item_price(item_list, item_name)
        
        if harga is not None:
            pesanan += (item_name, harga)
            total += harga
            print(f"Item '{item_name}' ditambahkan dengan harga {harga} IDR.")
            stack.push(item_name)
        else:
            print(f"Item '{item_name}' tidak ditemukan di menu.")
    
    print(f"\nTotal harga pesanan {nama_pembeli} adalah: {total} IDR")
    pesanan.display()

    while True:
        uang = int(input("Masukkan Pembayaran : "))
        if uang > total:
            print("kembalian", uang - total)
            break
        elif uang == total:
            print("uang pas")
            break
        else:
            print("uang kurang, masukkan lagi")
                
        
    queue.enqeue(nama_pembeli, pesanan, total)

    print("riwayat pesanan: ")
    stack.display()


def sort_menu():
    print("\nPilih pengurutan")
    print("1. urut berdasarkan nama item (a-z)")
    print("2. urut berdasarkan harga (termurah-termahal)")

    pilihan = input("pilih opsi 1/2")
    if pilihan == "1":
        item_list.bubble_sort(by='item')
        print("\nItem diurutkan berdasarkan nama (a-z)")
    elif pilihan == "2":
        item_list.bubble_sort(by='harga')
        print("\nitem diurutkan berdasarkan harga (termurah-termahalr)")
    else:
        print("tidak valid")

    print_daftar_harga(item_list) 




def main_menu():            #menu utama kasir
    queue = Queue(json_file='data_pemebelian.json')
    stack = Stack()
    while True:
        print("\nMenu Opsi:")
        print("1. Masukkan pesanan Anda")
        print("2. Tampilkan antrian")
        print("3. Urutan menu")
        print("4. Selesai Pesanan")
        
        pilihan = input("Pilih opsi (1,2,3,4): ")
        
        if pilihan == "1":
            print_daftar_harga(item_list)
            calculate_total(queue, stack)
    
        elif pilihan == "2":
            queue.display_queue()

        elif pilihan == "3":
            sort_menu()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan program kasir.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih opsi 1 atau 2.")


main_menu()
