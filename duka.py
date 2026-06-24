# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SYSTEM YA MAUZO - v1.0")
        self.root.geometry("400x320")
        self.root.configure(bg="#f4f6f9")
        self.root.resizable(False, False)

        header_login = tk.Frame(root, bg="#1a365d", height=50)
        header_login.pack(fill=tk.X)

        tk.Label(header_login, text="DUKA - DIGITAL PoS (VERSION 1.0)", font=("Aial", 14, "bold"), fg="white", bg="#1a365d").pack(pady=12)

        frame_inputs = tk.Frame(root,bg="#f4f6f9")
        frame_inputs.pack(pady=20)

        tk.Label(frame_inputs, text="Jina la Mtumiaji (Username):", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        self.ent_user = tk.Entry(frame_inputs, font=("Arial", 12), width=28)
        self.ent_user.pack(pady=5)

        tk.Label(frame_inputs, text="Nenosiri (Password):", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        self.ent_pass = tk.Entry(frame_inputs, show="*", font=("Arial", 12), width=28)
        self.ent_pass.pack(pady=5)

        tk.Button(root, text="INGIA", bg="#2b6cb0", fg="white", font=("Arial", 11, "bold"),
                  width=25, height=2, bd=0, cursor="hand2", command=self.thibitisha_data).pack(pady=10)

    def thibitisha_data(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Onyo!", "Tafadhali jaza jina na password!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="duka_db", use_pure=True
            )
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM watumiaji WHERE jina_la_mtumiaji = %s AND nywila = %s"
            cursor.execute(query, (username, password))
            mtumiaji = cursor.fetchone()

            cursor.close()
            conn.close()

            if mtumiaji:
                user_role = mtumiaji.get("cheo", "cashier").lower()
                messagebox.showinfo("Hongera!", f"Karibu sana {username}!\nUmeingia kama: {user_role.upper()}")

                self.root.destroy()

                root_kuu = tk.Tk()
                app = MfumoWaPOS(root_kuu, role=user_role)
                root_kuu.mainloop()
            else:
                messagebox.showerror("Kosa!", "Jina la mtumiaji au nenosiri sio sahihi!")

        except Exception as e:
            messagebox.showerror("Kosa la Mfumo!", f"Imefeli kuunganisha Mtumiaji:\nMaelezo: {str(e)}") 
                                         
class MfumoWaPOS:
    def __init__(self, root, role="cashier"):
        self.root = root
        self.user_role = role
        self.root.title("SYSTEM YA MAUZO - POINT OF SALE (POS) - v1.0")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f9")
        
        self.unganisha_database()

        self.var_tafuta = tk.StringVar()
        self.var_jina_bidhaa = tk.StringVar()
        self.var_bei = tk.StringVar()
        self.var_idadi = tk.StringVar()
        self.var_jumla_kuu = tk.DoubleVar(value=0.0)

        self.kapu_la_bidhaa = []
        self.namba_ya_risiti = ""
        self.id_bidhaa_iliyochaguliwa = None

        header = tk.Frame(root, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        lbl_kichwa = tk.Label(header, text="DUKA - DIGITAL POINT OF SALE(VERSION 1.0)", font=("Arial", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_kichwa.pack(pady=12)

        self.btn_admin_panel = tk.Button(header, text="PANELI YA ADMIN", bg="#e53e3e", fg="white",
                                         font=("Arial", 11, "bold"), bd=0, padx=10, cursor="hand2",
                                         command=self.fungua_paneli_ya_admin)
        if self.user_role =="admin":
            self.btn_admin_panel.pack(side=tk.RIGHT, padx=15,pady=10)

        main_frame = tk.Frame(self.root, bg="#f4f6f9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        frame_kushoto = tk.LabelFrame(main_frame, text=" Sehemu ya Muuzaji ", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50", bd=2)
        frame_kushoto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        lbl_tafuta = tk.Label(frame_kushoto, text="Tafuta bidhaa (Andika jina):", font=("Arial", 10, "bold"), bg="white")
        lbl_tafuta.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        entry_tafuta = tk.Entry(frame_kushoto, textvariable=self.var_tafuta, font=("Arial", 11), bd=2, width=25)
        entry_tafuta.grid(row=0, column=1, padx=10, pady=15)
        entry_tafuta.bind("<KeyRelease>", self.chagua_bidhaa_kutoka_stoo)

        lbl_jina = tk.Label(frame_kushoto, text="Bidhaa", font=("Aria", 10), bg="white")
        lbl_jina.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        entry_jina = tk.Entry(frame_kushoto, textvariable=self.var_jina_bidhaa, font=("Arial", 11), state="readonly", width=25)
        entry_jina.grid(row=1, column=1, padx=10, pady=10)

        lbl_bei = tk.Label(frame_kushoto, text="Bei ya Kuuza:", font=("Arial", 10), bg="white")
        lbl_bei.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        entry_bei = tk.Entry( frame_kushoto, textvariable=self.var_bei, font=("Arial", 11), state="readonly", width=25)
        entry_bei.grid(row=2, column=1, padx=10, pady=10)

        lbl_idadi = tk.Label(frame_kushoto, text="Ingiza Idadi:", font=("Arial", 10, "bold"), bg="white")
        lbl_idadi.grid(row=3, column=0, padx=15, pady=10, sticky="w")
        entry_idadi = tk.Entry(frame_kushoto, textvariable=self.var_idadi, font=("Arial", 11), bd=2, width=25)
        entry_idadi.grid(row=3, column=1, padx=10, pady=10)

        btn_weka_kapu = tk.Button(frame_kushoto, text="Weka Kwenye Kapu", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", bd=0, cursor="hand2", command=self.weka_kwenye_kapu)
        btn_weka_kapu.grid(row=4, columnspan=2, column=0, padx=15, pady=20, sticky="ew")

        self.tree_stoo = ttk.Treeview(frame_kushoto, columns=("id", "jina", "bei", "stoo"), show="headings", height=8)
        self.tree_stoo.grid(row=5, column=0, columnspan=2, padx=15, pady=10, sticky="nsew")

        self.tree_stoo.heading("id", text="ID")
        self.tree_stoo.heading("jina", text="Jina la Bidhaa")
        self.tree_stoo.heading("bei", text="Bei (TZS)")
        self.tree_stoo.heading("stoo", text="Iliyopo Stoo")

        self.tree_stoo.column("id", width=40, anchor="center")
        self.tree_stoo.column("jina", width=150)
        self.tree_stoo.column("bei", width=80, anchor="e")
        self.tree_stoo.column("stoo", width=80, anchor="center")
        self.tree_stoo.bind("<<TreeviewSelect>>", self.chagua_bidhaa_kutoka_stoo)

        frame_kulia = tk.LabelFrame(main_frame, text=" Kapu la Manunuzi ", font=("Aial", 12, "bold"), bg="white", fg="#2c3e50", bd=2)
        frame_kulia.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tree_kapu = ttk.Treeview(frame_kulia, columns=("jina", "bei", "idadi", "jumla"), show="headings", height=15)
        self.tree_kapu.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.tree_kapu.heading("jina", text="Bidhaa")
        self.tree_kapu.heading("bei", text="Bei ya Moja")
        self.tree_kapu.heading("idadi", text="Idadi")
        self.tree_kapu.heading("jumla", text="Jumla Kuu")

        self.tree_kapu.column("jina", width=150)
        self.tree_kapu.column("bei", width=90, anchor="e")
        self.tree_kapu.column("idadi", width=60, anchor="center")
        self.tree_kapu.column("jumla", width=100, anchor="e")

        frame_hesabu = tk.Frame(frame_kulia, bg="white")
        frame_hesabu.pack(fill=tk.X, padx=15, pady=10)

        lbl_total_text = tk.Label(frame_hesabu, text="JUMLA KUU (TZS):", font=("Arial", 14, "bold"), bg="white", fg="#c0392b")
        lbl_total_text.pack(side=tk.LEFT)

        self.lbl_total_namba = tk.Label(frame_hesabu, text="0.00", font=("Arial", 16, "bold"), bg="white", fg="#c0392b")
        self.lbl_total_namba.pack(side=tk.RIGHT)

        btn_piga_mauzo = tk.Button(frame_kulia, text="PIGA RISITI / MALIZA MAUZO", font=("Arial", 13, "bold"), bg="#2980b9", fg="white", bd=0, height=2, cursor="hand2", command=self.kamilisha_mauzo)
        btn_piga_mauzo.pack(fill=tk.X, padx=15, pady=15)

        self.pakia_bidhaa_stoo()

        if self.user_role == "cashier":
            if hasattr(self, 'btn_ripoti'):
                self.btn_ripoti.pack_forget()

            if hasattr(self, 'tab_admin'):
                self.notebook.tab(self.tab_admin, state="disabled")
                pass
    def unganisha_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="duka_db"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"Database imegoma kuunganisha! Hakikisha XAMPP imewaka. Maelezo: {e}")
    def pakia_bidhaa_stoo(self):
        for item in self.tree_stoo.get_children():
            self.tree_stoo.delete(item)

        self.cursor.execute("SELECT id, jina_la_bidhaa, bei_ya_kuuza, idadi_ya_stoo FROM bidhaa")
        for row in self.cursor.fetchall():
            bei_format = "{:,.2f}".format(row[2])
            self.tree_stoo.insert("", tk.END, values=(row[0],row[1], bei_format, row[3]))

    def chagua_bidhaa_kutoka_stoo(self,event):
        try:
            item_id = self.tree_stoo.selection()[0]
            vitu = self.tree_stoo.item(item_id, "values")
            self.id_bidhaa_iliyochaguliwa = vitu[0]
            self.var_jina_bidhaa.set(vitu[1])
            self.var_bei.set(vitu[2].replace(",", ""))
            self.var_idadi.set("1")
        except IndexError:
            pass
    def weka_kwenye_kapu(self):
        if self.var_jina_bidhaa.get() == "" or self.var_bei.get() == "":
            messagebox.showwarning("Onyo", "Ingiza bidhaa kwenye jedwari la stoo kwanza!")
            return
        
        try:
            idadi = int(self.var_idadi.get())
            if idadi <= 0:
                messagebox.showwarning("Onyo", "Idadi lazima ianzie 1 na kuendelea!")
                return
        except ValueError:
            messagebox.showwarning("onyo", "Tafadhali ingiza idadi halali ya namba!")
            
        jina = self.var_jina_bidhaa.get()
        bei = float(self.var_bei.get())
        jumla_ya_vitu = bei * idadi

        self.kapu_la_bidhaa.append({
            "id": self.id_bidhaa_iliyochaguliwa,
            "jina": jina,
            "bei": bei,
            "idadi": idadi,
            "jumla": jumla_ya_vitu
        })
        
        self.tree_kapu.insert("", tk.END, values=(jina, "{:,.2f}".format(bei), idadi, "{:,.2f}".format(jumla_ya_vitu)))

        self.var_jumla_kuu.set(self.var_jumla_kuu.get() + jumla_ya_vitu)
        self.lbl_total_namba.config(text="{:,.2f}".format(self.var_jumla_kuu.get()))

        self.var_jina_bidhaa.set("")
        self.var_bei.set("")
        self.var_idadi.set("")
    def kamilisha_mauzo(self):
        if not self.kapu_la_bidhaa:
            messagebox.showwarning("Onyo", "Kapu lipo wazi! Weka bidhaa kabla ya kupiga risiti.")
            return

        try:
            import random
            import datetime

            namba_ya_risiti = "RST" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            for kitu in self.kapu_la_bidhaa:
                query_mauzo = """
                      INSERT INTO mauzo (namba_ya_risiti, id_ya_bidhaa, idadi_iliyozuiliwa, jumla_ya_bei)
                      VALUES (%s, %s, %s, %s)
                """

                self.cursor.execute(query_mauzo, (namba_ya_risiti, kitu["id"], kitu["idadi"], kitu["jumla"]))

                query_update_stoo = "UPDATE bidhaa SET idadi_ya_stoo = idadi_ya_stoo - %s WHERE id = %s"
                self.cursor.execute(query_update_stoo, (kitu["idadi"], kitu["id"]))

            self.conn.commit()
            messagebox.showinfo("Hongera!", f"Mauzo yamekamilika kikamilifu!\nNamba ya Risiti: {self.namba_ya_risiti}")

            vitu_vya_risiti = list(self.kapu_la_bidhaa)

            self.onyesha_risiti_window(namba_ya_risiti, vitu_vya_risiti)

            self.kapu_la_bidhaa.clear()
            for item in self.tree_kapu.get_children():
                self.tree_kapu.delete(item)
                
            self.var_jumla_kuu.set("0.00")
            if hasattr(self, 'lbl_total_namba'):
                self.lbl_total_namba.config(text="0.00")
            
            self.pakia_bidhaa_stoo()

            self.sasisha_ripoti_za_admin()
            self.sasisha_tathmini_ya_bidhaa()


        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Kuna kitu kimefeli wakati wa kuhifadhi mauzo: {e}")

    def sasisha_ripoti_za_admin(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="duka_db")
            cursor = conn.cursor()
                        
            cursor.execute("SELECT SUM(jumla_ya_bei) FROM mauzo")
            matokeo_pesa = cursor.fetchone()[0]
            jumla_ya_mauzo_yote = float(matokeo_pesa) if matokeo_pesa is not None else 0.0
            if hasattr(self, 'lbl_jumla_sales'):
                self.lbl_jumla_sales.config(text=f"TZS {jumla_ya_mauzo_yote:,.2f}")
                        
            cursor.execute("SELECT COUNT(DISTINCT id_ya_bidhaa) FROM mauzo")
            jumla_miamala = cursor.fetchone()[0]
            if hasattr(self, 'lbl_jumla_miamala'):
                self.lbl_jumla_miamala.config(text=str(jumla_miamala))
                       
            if hasattr(self, 'tree_ripoti'): 
                for item in self.tree_ripoti.get_children():
                    self.tree_ripoti.delete(item)
                        
            query_mauzo = "SELECT id_ya_bidhaa, SUM(idadi_iliyozuiliwa) AS jumla_idadi, SUM(jumla_ya_bei) AS mshiko_wote FROM mauzo GROUP BY id_ya_bidhaa"

            cursor.execute(query_mauzo)
            maulizo_yote = cursor.fetchall()
                        
            for mstari in maulizo_yote:
                id_bidhaa = mstari[0],
                jumla_idadi = int(mstari[1]) if mstari[1] is not None else 0
                pesa_iliyokusanywa = float(mstari[2])if mstari[2] is not None else 0.0
                       
                jina_la_bidhaa = f"Bidhaa ID: {id_bidhaa}"

                cursor.execute("SELECT jina_la_bidhaa, bei_ya_kuuza FROM bidhaa WHERE id = %s", (id_bidhaa))
                res_bidhaa = cursor.fetchone()
                if res_bidhaa:
                    if res_bidhaa[0] is not None:
                        jina_la_bidhaa = res_bidhaa[0]
                    if res_bidhaa[1]  is not None:
                        bei_ya_kila_moja = float(res_bidhaa[1])

                if bei_ya_kila_moja == 0.00 and jumla_idadi > 0:
                            bei_ya_kila_moja == pesa_iliyokusanywa / jumla_idadi
                        
                bei_formatted = f"TZS {bei_ya_kila_moja:,.2f}"
                jumla_formatted = f"TZS{pesa_iliyokusanywa:,.2f}"
                        
                self.tree_ripoti.insert("", tk.END, values=(
                    id_bidhaa,
                    jina_la_bidhaa,
                    bei_formatted,
                    jumla_idadi,
                    jumla_formatted
                ))
                         
            cursor.close()
            conn.close()
        except Exception as ex:
            print(f"Imefeli kusoma ripoti: {ex}")
            messagebox.showerror("Kosa la Ripoti", f"Imefeli kusoma ripoti:\n{ex}")
    def sasisha_tathmini_ya_bidhaa(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="duka_db")
            cursor = conn.cursor()
                
            for item in self.tree_tathmini.get_children():
                self.tree_tathmini.delete(item)
                    
            self.tree_tathmini.tag_configure("faida_kubwa", background="#d4edda", foreground="#155724")
            self.tree_tathmini.tag_configure("faida_wastani", background="#fff3cd", foreground="#856404")
            self.tree_tathmini.tag_configure("faida_ndogo", background="#f8d7da", foreground="#721c24")

            query_tathmini = "SELECT m.id_ya_bidhaa, b.jina_la_bidhaa, b.bei_ya_kuuza, b.bei_ya_kununua, SUM(m.idadi_iliyozuiliwa) AS jumla_idadi, SUM(m.jumla_ya_bei) AS mshiko_wote, b.idadi_ya_stoo FROM mauzo m INNER JOIN bidhaa b ON m.id_ya_bidhaa = b.id GROUP BY m.id_ya_bidhaa"
           
            cursor.execute(query_tathmini)
            data_zote = cursor.fetchall()
                
            for mstari in data_zote:
                id_bidhaa = mstari[0]
                jina_bidhaa = mstari[1]
                bei_kuuza = float(mstari[2]) if mstari[2] is not None else 0.0
                bei_kununua = float(mstari[3]) if mstari[3] is not None else 0.0
                idadi_iliyouzwa = int(mstari[4]) if mstari[4] is not None else 0
                pesa_iliyokusanywa = float(mstari[5]) if mstari[5] is not None else 0.0
                stoki_iliyobaki = int(mstari[6]) if mstari[6] is not None else 0
                    
                gharama_ya_mtaji = bei_kununua * idadi_iliyouzwa
                faida_halisi = pesa_iliyokusanywa - gharama_ya_mtaji
                    
                if stoki_iliyobaki <= 0:
                    hali_stoki = "IMEISHA VITI!"
                elif stoki_iliyobaki <= 10:
                        hali_stoki = f"Inatahadharisha ({stoki_iliyobaki})"
                else:
                    hali_stoki = f"Inatosha ({stoki_iliyobaki})"
                    
                if faida_halisi >= 50000:
                    kikundi_cha_rangi = "faida_kubwa"
                elif 10000 <= faida_halisi < 50000:
                    kikundi_cha_rangi = "faida_wastani"
                else:
                    kikundi_cha_rangi = "faida_ndogo"
                    
                bei_formatted = f"TZS {bei_kuuza:,.2f}"
                faida_formatted = f"TZS {faida_halisi:,.2f}"
                    
                self.tree_tathmini.insert("", tk.END, values=(
                    id_bidhaa,
                    jina_bidhaa,
                    idadi_iliyouzwa,
                    bei_formatted,
                    faida_formatted,
                    hali_stoki
                ), tags=(kikundi_cha_rangi,))
                    
            cursor.close()
            conn.close()
        except Exception as ex:
            print(f"Error ya tathmini: {ex}")
            messagebox.showerror("Kosa la Tathmini", f"Imefeli kupiga hesabu za tathmini:\n{ex}")
 
            
    def onyesha_risiti_window(self, namba_ya_risiti, vitu_vya_risiti):
        
        import datetime
        import tkinter as tk
        
        risiti_win = tk.Toplevel(self.root)
        risiti_win.title("Risiti ya Mauzo")
        risiti_win.geometry("400x570")
        risiti_win.configure(bg="white")
        risiti_win.resizable(False, False)

        mstari = "-" * 38 + "\n"
        nyota = "*" * 38 + "\n"

        risiti_text = nyota
        risiti_text += "      SAM-NCTECH INVESTMENT     \n"
        risiti_text += "        MOROGORO, TANZANIA    \n"
        risiti_text += nyota
        risiti_text += f"Risiti No: {namba_ya_risiti}\n"
        risiti_text += f"Tarehe: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M%S')}\n"
        risiti_text += mstari
        risiti_text += f"{'Item':<15}{'Qty':<6}{'Price':<8}{'Total':<9}\n"
        risiti_text += mstari

        jumla_kuu = 0
        for kitu in vitu_vya_risiti:
            jina_bidhaa = kitu.get('jina') or kitu.get('bidhaa') or kitu.get('jina_bidhaa') or "Bidhaa"
            idadi = int(kitu.get('idadi', 1))
            bei_moja = float(kitu.get('bei') or kitu.get('bei_moja', 0))
            bei_jumla = float(kitu.get('jumla') or (idadi * bei_moja))
            
            jumla_kuu += bei_jumla
            jina_fupi = jina_bidhaa[:13]
            risiti_text += f"{jina_fupi:<15}{idadi:<6}{bei_moja:<8.0f}{bei_jumla:<9.0f}\n"

        risiti_text += mstari
        risiti_text += f"JUMLA KUU            TZS{jumla_kuu:.2f}\n"
        risiti_text += mstari
        risiti_text += "     ASANTE KWA AJILI YA MAUZO\n"
        risiti_text += "        KARIBU TENA TENA\n"
        risiti_text += nyota
        
        text_area = tk.Text(risiti_win, width=45, height=22, font=("Courier", 9), bg="#f9f9f9", fg="black", bd=0)
        text_area.pack(pady=10)
        text_area.insert(tk.END, risiti_text)
        text_area.config(state=tk.DISABLED)

        fremu_vifungo = tk.Frame(risiti_win, bg="white")
        fremu_vifungo.pack(pady=5)

        btn_save = tk.Button(fremu_vifungo, text="SAVE RISITI", font=("Arial", 9, "bold"), bg="#5cb85c", fg="white",
                           command=lambda: self.save_risiti_faili(risiti_text, namba_ya_risiti), padx=5, pady=5)
        btn_save.pack(side=tk.LEFT, padx=5)

        btn_print = tk.Button(fremu_vifungo, text="PRINT RISITI", font=("Arial", 9, "bold"), bg="#f0ad4e", fg="white",
                              command=lambda: self.print_risiti_mashine(risiti_text), padx=5, pady=5)
        btn_print.pack(side=tk.LEFT, padx=5)

        btn_funga = tk.Button(risiti_win, text="FUNGA RISITI", font=("Arial", 9, "bold"), bg="#d9534f", fg="white",
                              command=risiti_win.destroy, padx=5, pady=5)
        btn_funga.pack(side=tk.LEFT, padx=5)

    def save_risiti_faili(self, risiti_text, namba_ya_risiti):
        from tkinter import filedialog, messagebox
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        faili_path = filedialog.asksaveasfilename(
            initialfile=f"Risiti_{namba_ya_risiti}.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if faili_path:
            try:
                c= canvas.Canvas(faili_path, padesize=letter)
                c.setFont=("Courier", 10)

                y = 750
                for line in risiti_text.split("\n"):
                    c.drawString(50, y, line)
                    y -=15
                    if y <50:
                        c.ShowPage()
                        c.setFont("Courier", 10)
                        y = 750
                c.save()
                messagebox.showinfo("Hongera!", "Risiti imehifadhiwa kikamilifi!")
            except Exception as e:
                messagebox.showerror("Kosa!", f"Imeshindwa kusave: {str(e)}")

    def print_risiti_mashine(self, risiti_text):
        from tkinter import messagebox
        try:
            import win32print
            import win32ui
            import win32con

            printer_jina = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_jina)
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_jina)

            hdc.StartDoc("Risiti ya Mauzo")
            hdc.StartPage()
            hdc.SetMapMode(win32con.MM_TEXT)

            font = win32ui.CreateFont({
                "name": "Courier New",
                "height": 16,
                "weight": 400
            })
            hdc.SelectObject(font)

            y = 10
            for mstari in risiti_text.split("\n"):
                hdc.TextOut(10, y, mstari)
                y += 20

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            win32print.ClosePrinter(hprinter)

            messagebox.showinfo("Honfera!", "Risiti Imetumwa kwente printa!")
        except Exception as e:
            messagebox.showerror("kosa!", f"Imefeli kuprint: {str(e)}")
            
    def fungua_paneli_ya_admin(self):
        top_admin = tk.Toplevel(self.root)
        top_admin.title("DUKA - DIGITAL POS - Paneli ya Usimamizi")
        top_admin.geometry("750x500")
        top_admin.configure(bg="#f4f6f9")

        notebook = ttk.Notebook(top_admin)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tab_ripoti = tk.Frame(notebook, bg="white")
        notebook.add(tab_ripoti, text=" Ripoti ya Mauzo ")

        self.tab_tathmini = tk.Frame(notebook, bg="white")
        notebook.add(self.tab_tathmini, text="Tathmini ya Bidhaa")
 
        tab_users = tk.Frame(notebook, bg="white")
        notebook.add(tab_users, text=" Sajiri Watumiaji ")

        tk.Label(tab_users, text="Sajiri Mfanyakazi Mpya", font=("Arial", 13, "bold"), bg="white", fg="#1a365d").pack(pady=10)

        frame_form = tk.Frame(tab_users, bg="white")
        frame_form.pack(pady=20)

        tk.Label(frame_form, text="Jina la Mtumiaji (Username):", bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ent_new_user = tk.Entry(frame_form, font=("Arial", 11), width=25, bd=2, relief=tk.SUNKEN)
        ent_new_user.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame_form, text="Nenosiri (password):", font=("Arial", 11), bg="white").grid(row=1, column=0,padx=10, pady=10, sticky="w")
        ent_new_pass = tk.Entry(frame_form, font=("Arial", 11), show="*", width=25, bd=2, relief=tk.SUNKEN)
        ent_new_pass.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame_form, text="Cheo (Role):", font=("Arial", 11), bg="white").grid(row=2, column=0,padx=10, pady=10, sticky="w")
        cmb_role = ttk.Combobox(frame_form, values=["Admin", "cashier"], font=("Arial", 10), state="readonly", width=23)
        cmb_role.grid(row=2, column=1, padx=10, pady=10)
        cmb_role.set("cashier")

        tk.Label(tab_ripoti, text="Ripoti ya Mauzo na Miamala ya Leo", font=("Arial", 14, "bold"), bg="white", fg="#1a365d").pack(pady=10)
        
        frame_cards = tk.Frame(tab_ripoti, bg="white")
        frame_cards.pack(pady=5, fill=tk.X, padx=20)
        
        card1 = tk.Frame(frame_cards, bg="#ebf8ff", bd=1, relief=tk.GROOVE)
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, ipady=10)
        tk.Label(card1, text="Jumla ya Mauzo ya Leo", font=("Arial", 10), bg="#ebf8ff", fg="#2b6cb0").pack(pady=2)
        self.lbl_jumla_sales = tk.Label(card1, text="TZS 0.00", font=("Arial", 14, "bold"), bg="#ebf8ff", fg="#2b6cb0")
        self.lbl_jumla_sales.pack()
        
        card2 = tk.Frame(frame_cards, bg="#f0fff4", bd=1, relief=tk.GROOVE)
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, ipady=10)
        tk.Label(card2, text="Jumla ya Miamala", font=("Arial", 10), bg="#f0fff4", fg="#38a169").pack(pady=2)
        self.lbl_jumla_miamala = tk.Label(card2, text="0", font=("Arial", 14, "bold"), bg="#f0fff4", fg="#38a169")
        self.lbl_jumla_miamala.pack()
        
        frame_table = tk.Frame(tab_ripoti, bg="white")
        frame_table.pack(pady=15, fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(frame_table, text="Orodha ya Bidhaa Zilizotoka:", font=("Arial", 11, "bold"), bg="white", fg="#4a5568").pack(anchor="w", pady=5)
        
        columns_ripoti = ("id", "bidhaa", "idadi", "bei", "jumla")
        self.tree_ripoti = ttk.Treeview(frame_table, columns=columns_ripoti, show="headings", height=10)
        
        self.tree_ripoti.heading("id", text="ID")
        self.tree_ripoti.heading("bidhaa", text="Jina la Bidhaa")
        self.tree_ripoti.heading("idadi", text="Idadi")
        self.tree_ripoti.heading("bei", text="Bei ya Kila Moja")
        self.tree_ripoti.heading("jumla", text="Jumla Kuu (TZS)")
        
        self.tree_ripoti.column("id", width=80, anchor="center")
        self.tree_ripoti.column("bidhaa", width=250, anchor="w")
        self.tree_ripoti.column("idadi", width=80, anchor="center")
        self.tree_ripoti.column("bei", width=130, anchor="e")
        self.tree_ripoti.column("jumla", width=150, anchor="e")
        
        scrollbar_ripoti = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree_ripoti.yview)
        self.tree_ripoti.configure(yscrollcommand=scrollbar_ripoti.set)
        
        self.tree_ripoti.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_ripoti.pack(side=tk.RIGHT, fill=tk.Y)

        frame_tathmini_meza = tk.Frame(self.tab_tathmini, bg="white")
        frame_tathmini_meza.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        lbl_tathmini_title = tk.Label(
            frame_tathmini_meza, 
            text="Tathmini ya Mauzo: Bidhaa Zinazoleta Faida na Hali ya Stoki", 
            font=("Helvetica", 14, "bold"), 
            bg="white", 
            fg="#2c3e50"
        )
        lbl_tathmini_title.pack(anchor=tk.W, pady=(0, 10))
        
        
        columns_tathmini = ("id", "jina", "idadi_iliyouzwa", "bei_ya_kuuza", "faida", "hali_stoki")
        
       
        self.tree_tathmini = ttk.Treeview(frame_tathmini_meza, columns=columns_tathmini, show="headings")
        
        self.tree_tathmini.heading("id", text="ID ya Bidhaa")
        self.tree_tathmini.heading("jina", text="Jina la Bidhaa")
        self.tree_tathmini.heading("idadi_iliyouzwa", text="Jumla Iliyouzwa (Kilo/Pcs)")
        self.tree_tathmini.heading("bei_ya_kuuza", text="Bei ya Kuuza (1)")
        self.tree_tathmini.heading("faida", text="Faida Iliyoingia (TZS)")
        self.tree_tathmini.heading("hali_stoki", text="Hali ya Stoki Dukanani")
        
        self.tree_tathmini.column("id", width=100, anchor=tk.CENTER)
        self.tree_tathmini.column("jina", width=220, anchor=tk.W)
        self.tree_tathmini.column("idadi_iliyouzwa", width=160, anchor=tk.CENTER)
        self.tree_tathmini.column("bei_ya_kuuza", width=150, anchor=tk.CENTER)
        self.tree_tathmini.column("faida", width=180, anchor=tk.CENTER)
        self.tree_tathmini.column("hali_stoki", width=160, anchor=tk.CENTER)
        
        scroll_y_tathmini = ttk.Scrollbar(frame_tathmini_meza, orient=tk.VERTICAL, command=self.tree_tathmini.yview)
        self.tree_tathmini.configure(yscrollcommand=scroll_y_tathmini.set)
        
        scroll_y_tathmini.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tathmini.pack(fill=tk.BOTH, expand=True)
        
        def save_user_to_db():
            u = ent_new_user.get().strip()
            p = ent_new_pass.get().strip()
            c = cmb_role.get()

            if not u or not p:
                messagebox.showwarning("kosa!", "Tafadhali jaza nafasi zote!")
                return

            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="duka_db")
                cursor = conn.cursor()
                sql = "INSERT INTO watumiaji (jina_la_mtumiaji, nywila, cheo) VALUES (%s, %s, %s)"
                cursor.execute(sql, (u, p, c))
                conn.commit()
                cursor.close()
                messagebox.showinfo("Hongera!", f"Mtumiaji '{u}' amesajiliwa!")
                ent_new_user.delete(0, tk.END)
                ent_new_pass.delete(0, tk.END)
            except Exception as ex:
                messagebox.showerror("Kosa la SQL", f"Maelezo: {ex}")
        tk.Button(frame_form, text="HIFADHI MFANYAKAZI", bg="#2b6cb0", fg="white",
            font=("Arial", 11, "bold"), bd=0, padx=20, pady=8, cursor="hand2",
            command=save_user_to_db).grid(row=3, column=0, columnspan=2, pady=20)
        
 
if __name__ == "__main__":
    root_login = tk.Tk()
    washa_login = LoginWindow(root_login)
    root_login.mainloop() 


    
                              

