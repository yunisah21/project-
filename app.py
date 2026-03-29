from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'edupathen_secret_key_2025_secure'
bcrypt = Bcrypt(app)

# --- KONFIGURASI DATABASE ---
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="minat_bakat_db",
            autocommit=False,
            buffered=True  # Fix "Unread result found" error
        )
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        print("⚠️  Pastikan:")
        print("   1. XAMPP MySQL sudah berjalan")
        print("   2. Database 'minat_bakat_db' sudah dibuat")
        print("   3. Tabel sudah diimport dari SQL file")
        return None

# --- DATA PERTANYAAN TES MINAT (15 Pertanyaan) ---
PERTANYAAN_MINAT = [
    {
        'nomor': 1,
        'pertanyaan': 'Kamu lebih suka apa?',
        'pilihan_a': 'Kegiatan yang membutuhkan aktivitas fisik',
        'pilihan_b': 'Kegiatan yang menggunakan pikiran',
        'kategori_a': 'fisik',
        'kategori_b': 'pikiran'
    },
    {
        'nomor': 2,
        'pertanyaan': 'Saat waktu luang, kamu lebih memilih?',
        'pilihan_a': 'Membaca buku atau artikel',
        'pilihan_b': 'Menonton film atau video',
        'kategori_a': 'verbal',
        'kategori_b': 'visual'
    },
    {
        'nomor': 3,
        'pertanyaan': 'Kamu lebih tertarik dengan?',
        'pilihan_a': 'Bekerja dengan data dan angka',
        'pilihan_b': 'Bekerja dengan orang dan komunikasi',
        'kategori_a': 'analitis',
        'kategori_b': 'sosial'
    },
    {
        'nomor': 4,
        'pertanyaan': 'Dalam mengerjakan tugas, kamu lebih suka?',
        'pilihan_a': 'Bekerja sendiri dan mandiri',
        'pilihan_b': 'Bekerja dalam tim',
        'kategori_a': 'individual',
        'kategori_b': 'kolaboratif'
    },
    {
        'nomor': 5,
        'pertanyaan': 'Kamu lebih tertarik pada pekerjaan yang?',
        'pilihan_a': 'Kreatif dan inovatif',
        'pilihan_b': 'Sistematis dan terstruktur',
        'kategori_a': 'kreatif',
        'kategori_b': 'sistematis'
    },
    {
        'nomor': 6,
        'pertanyaan': 'Saat belajar hal baru, kamu lebih suka?',
        'pilihan_a': 'Praktek langsung',
        'pilihan_b': 'Memahami teori dulu',
        'kategori_a': 'praktis',
        'kategori_b': 'teoritis'
    },
    {
        'nomor': 7,
        'pertanyaan': 'Kamu lebih tertarik dengan?',
        'pilihan_a': 'Seni dan desain',
        'pilihan_b': 'Sains dan teknologi',
        'kategori_a': 'artistik',
        'kategori_b': 'teknis'
    },
    {
        'nomor': 8,
        'pertanyaan': 'Dalam memecahkan masalah, kamu lebih suka?',
        'pilihan_a': 'Cara yang sudah terbukti',
        'pilihan_b': 'Cara baru yang belum dicoba',
        'kategori_a': 'konvensional',
        'kategori_b': 'eksperimental'
    },
    {
        'nomor': 9,
        'pertanyaan': 'Kamu lebih menikmati?',
        'pilihan_a': 'Pekerjaan di dalam ruangan',
        'pilihan_b': 'Pekerjaan di luar ruangan',
        'kategori_a': 'indoor',
        'kategori_b': 'outdoor'
    },
    {
        'nomor': 10,
        'pertanyaan': 'Kamu lebih tertarik dengan bidang?',
        'pilihan_a': 'Bisnis dan kewirausahaan',
        'pilihan_b': 'Pendidikan dan pengajaran',
        'kategori_a': 'bisnis',
        'kategori_b': 'edukatif'
    },
    {
        'nomor': 11,
        'pertanyaan': 'Dalam bekerja, kamu lebih memilih?',
        'pilihan_a': 'Jadwal yang fleksibel',
        'pilihan_b': 'Jadwal yang teratur dan pasti',
        'kategori_a': 'fleksibel',
        'kategori_b': 'terstruktur'
    },
    {
        'nomor': 12,
        'pertanyaan': 'Kamu lebih tertarik pada?',
        'pilihan_a': 'Membantu orang lain',
        'pilihan_b': 'Mencapai target pribadi',
        'kategori_a': 'altruistik',
        'kategori_b': 'ambisius'
    },
    {
        'nomor': 13,
        'pertanyaan': 'Saat menghadapi tantangan, kamu lebih suka?',
        'pilihan_a': 'Tantangan fisik',
        'pilihan_b': 'Tantangan mental',
        'kategori_a': 'fisik',
        'kategori_b': 'mental'
    },
    {
        'nomor': 14,
        'pertanyaan': 'Kamu lebih menikmati pekerjaan yang?',
        'pilihan_a': 'Rutin dan dapat diprediksi',
        'pilihan_b': 'Bervariasi dan dinamis',
        'kategori_a': 'rutin',
        'kategori_b': 'dinamis'
    },
    {
        'nomor': 15,
        'pertanyaan': 'Dalam karir, yang lebih penting bagimu?',
        'pilihan_a': 'Stabilitas dan keamanan',
        'pilihan_b': 'Pertumbuhan dan tantangan',
        'kategori_a': 'stabil',
        'kategori_b': 'progresif'
    }
]

# --- DATA PERTANYAAN TES BAKAT (15 Pertanyaan) ---
PERTANYAAN_BAKAT = [
    {'nomor': 1, 'pertanyaan': 'Saya percaya diri ketika memimpin suatu kegiatan atau diskusi.'},
    {'nomor': 2, 'pertanyaan': 'Saya senang berbicara atau menjelaskan sesuatu kepada orang lain.'},
    {'nomor': 3, 'pertanyaan': 'Saya mudah memahami dan mengingat kata-kata atau istilah baru.'},
    {'nomor': 4, 'pertanyaan': 'Saya lebih suka menyelesaikan masalah dengan logika dan analisis.'},
    {'nomor': 5, 'pertanyaan': 'Saya dapat dengan mudah membayangkan bentuk 3D atau pola visual.'},
    {'nomor': 6, 'pertanyaan': 'Saya peka terhadap ritme, melodi, dan nada musik.'},
    {'nomor': 7, 'pertanyaan': 'Saya menikmati aktivitas fisik seperti olahraga atau menari.'},
    {'nomor': 8, 'pertanyaan': 'Saya mudah memahami perasaan dan emosi orang lain.'},
    {'nomor': 9, 'pertanyaan': 'Saya sering merenungkan dan memahami diri saya sendiri.'},
    {'nomor': 10, 'pertanyaan': 'Saya tertarik mengamati fenomena alam dan lingkungan sekitar.'},
    {'nomor': 11, 'pertanyaan': 'Saya dapat dengan mudah mengatur dan mengoordinasi tim.'},
    {'nomor': 12, 'pertanyaan': 'Saya senang menulis cerita, puisi, atau artikel.'},
    {'nomor': 13, 'pertanyaan': 'Saya cepat dalam menghitung dan memecahkan soal matematika.'},
    {'nomor': 14, 'pertanyaan': 'Saya sering menggambar, melukis, atau mendesain sesuatu.'},
    {'nomor': 15, 'pertanyaan': 'Saya merasa nyaman bekerja dengan tangan dalam aktivitas praktis.'}
]

# --- ROUTE BERANDA ---
@app.route('/')
def index():
    return render_template('index.html')

# --- ROUTE MENU TES ---
@app.route('/menu-tes')
def menu_tes():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    return render_template('menu_tes.html')

# --- ROUTE REGISTER ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username dan password tidak boleh kosong!', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password minimal 6 karakter!', 'danger')
            return render_template('register.html')
        
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        db = get_db_connection()
        if db is None:
            flash('Koneksi database gagal!', 'danger')
            return render_template('register.html')
        
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            db.commit()
            flash('Registrasi Berhasil! Silakan Login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username sudah digunakan!', 'danger')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            db.close()
    
    return render_template('register.html')

# --- ROUTE LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username dan password tidak boleh kosong!', 'danger')
            return render_template('login.html')
        
        db = get_db_connection()
        if db is None:
            flash('Koneksi database gagal!', 'danger')
            return render_template('login.html')
        
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.check_password_hash(user['password'], password):
                session['user_id'] = user['id_user']
                session['username'] = user['username']
                flash(f'Selamat datang, {user["username"]}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Username atau Password salah!', 'danger')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            db.close()
    
    return render_template('login.html')

# --- ROUTE TES MINAT ---
@app.route('/tes-minat')
def tes_minat():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    return render_template('tes_minat.html', pertanyaan=PERTANYAAN_MINAT)

# --- ROUTE SUBMIT TES MINAT ---
@app.route('/submit-minat', methods=['POST'])
def submit_minat():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    
    # Ambil semua jawaban
    jawaban = {}
    kategori_count = {}
    
    for i in range(1, 16):
        jawaban_key = f'minat_{i}'
        jawaban_value = request.form.get(jawaban_key)
        
        if jawaban_value:
            jawaban[i] = jawaban_value
            # Hitung kategori
            if jawaban_value not in kategori_count:
                kategori_count[jawaban_value] = 0
            kategori_count[jawaban_value] += 1
    
    # Validasi semua soal dijawab
    if len(jawaban) < 15:
        flash('Mohon jawab semua pertanyaan!', 'warning')
        return redirect(url_for('tes_minat'))
    
    # Tentukan hasil berdasarkan kategori terbanyak
    kategori_dominan = max(kategori_count, key=kategori_count.get)
    total_skor = kategori_count[kategori_dominan]
    
    # Mapping hasil
    hasil_mapping = {
        'fisik': {
            'judul': 'Tipe Realistis & Praktis',
            'desc': 'Kamu memiliki minat pada pekerjaan yang melibatkan aktivitas fisik, menggunakan alat, atau bekerja di luar ruangan. Cocok untuk bidang seperti teknik, pertanian, atau olahraga.'
        },
        'pikiran': {
            'judul': 'Tipe Investigatif & Analitis',
            'desc': 'Kamu tertarik pada pekerjaan yang membutuhkan pemikiran analitis dan pemecahan masalah. Cocok untuk bidang seperti penelitian, sains, atau teknologi informasi.'
        },
        'kreatif': {
            'judul': 'Tipe Artistik & Kreatif',
            'desc': 'Kamu memiliki minat pada pekerjaan yang melibatkan kreativitas, seni, dan ekspresi diri. Cocok untuk bidang seperti desain, musik, atau penulisan.'
        },
        'sosial': {
            'judul': 'Tipe Sosial & Komunikatif',
            'desc': 'Kamu tertarik pada pekerjaan yang melibatkan interaksi dengan orang lain dan membantu mereka. Cocok untuk bidang seperti pendidikan, konseling, atau pelayanan sosial.'
        },
        'bisnis': {
            'judul': 'Tipe Enterprising & Persuasif',
            'desc': 'Kamu memiliki minat pada pekerjaan yang melibatkan kepemimpinan, persuasi, dan bisnis. Cocok untuk bidang seperti manajemen, marketing, atau kewirausahaan.'
        }
    }
    
    # Ambil hasil berdasarkan kategori dominan atau default
    hasil = hasil_mapping.get(kategori_dominan, {
        'judul': 'Tipe Eksploratif & Kreatif',
        'desc': 'Kamu adalah tipe orang yang suka eksplorasi dan mencoba hal-hal baru. Terus kembangkan minatmu!'
    })
    
    # Simpan ke database
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        try:
            # Insert hasil tes
            cursor.execute(
                "INSERT INTO hasil_tes (id_user, jenis_tes, total_skor, kategori_hasil, deskripsi_hasil) VALUES (%s, %s, %s, %s, %s)",
                (session['user_id'], 'minat', total_skor, hasil['judul'], hasil['desc'])
            )
            id_hasil = cursor.lastrowid
            
            # Insert detail jawaban
            for nomor, jawaban_value in jawaban.items():
                cursor.execute(
                    "INSERT INTO jawaban_tes (id_hasil, nomor_soal, jawaban) VALUES (%s, %s, %s)",
                    (id_hasil, nomor, jawaban_value)
                )
            
            db.commit()
            session['hasil_id'] = id_hasil
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    
    return redirect(url_for('hasil', jenis='minat'))

# --- ROUTE TES BAKAT ---
@app.route('/tes-bakat')
def tes_bakat():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    return render_template('tes_bakat.html', pertanyaan=PERTANYAAN_BAKAT)

# --- ROUTE SUBMIT TES BAKAT ---
@app.route('/submit-bakat', methods=['POST'])
def submit_bakat():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    
    # Ambil semua jawaban dan hitung total
    jawaban = {}
    total_skor = 0
    
    for i in range(1, 16):
        jawaban_key = f'bakat_{i}'
        jawaban_value = request.form.get(jawaban_key)
        
        if jawaban_value:
            jawaban[i] = int(jawaban_value)
            total_skor += int(jawaban_value)
    
    # Validasi semua soal dijawab
    if len(jawaban) < 15:
        flash('Mohon jawab semua pertanyaan!', 'warning')
        return redirect(url_for('tes_bakat'))
    
    # Tentukan hasil berdasarkan total skor
    if total_skor >= 68:
        kategori = "Kecerdasan Majemuk Tinggi"
        deskripsi = "Kamu memiliki bakat yang sangat baik dalam berbagai bidang. Kamu unggul dalam kecerdasan linguistik, logis-matematis, spasial, dan interpersonal. Kamu mudah beradaptasi dengan berbagai situasi dan dapat mengembangkan karir di berbagai bidang."
    elif total_skor >= 53:
        kategori = "Kecerdasan Majemuk Sedang"
        deskripsi = "Kamu memiliki bakat yang cukup baik di beberapa bidang. Fokus pada mengembangkan kekuatan utamamu sambil terus meningkatkan kemampuan di bidang lain. Kamu cocok untuk karir yang membutuhkan keseimbangan berbagai keterampilan."
    else:
        kategori = "Kecerdasan Spesifik"
        deskripsi = "Kamu memiliki bakat khusus di bidang tertentu. Fokuskan pengembangan pada area yang kamu kuasai dan minati. Dengan konsentrasi yang tepat, kamu dapat menjadi ahli di bidang spesifik tersebut."
    
    # Simpan ke database
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        try:
            # Insert hasil tes
            cursor.execute(
                "INSERT INTO hasil_tes (id_user, jenis_tes, total_skor, kategori_hasil, deskripsi_hasil) VALUES (%s, %s, %s, %s, %s)",
                (session['user_id'], 'bakat', total_skor, kategori, deskripsi)
            )
            id_hasil = cursor.lastrowid
            
            # Insert detail jawaban
            for nomor, nilai in jawaban.items():
                cursor.execute(
                    "INSERT INTO jawaban_tes (id_hasil, nomor_soal, jawaban) VALUES (%s, %s, %s)",
                    (id_hasil, nomor, str(nilai))
                )
            
            db.commit()
            session['hasil_id'] = id_hasil
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    
    return redirect(url_for('hasil', jenis='bakat'))

# --- ROUTE HASIL ---
@app.route('/hasil/<jenis>')
def hasil(jenis):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    
    nama = session['username']
    judul = "Hasil Tes"
    deskripsi = "Belum ada hasil tes."
    
    # Ambil hasil terbaru dari database
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT kategori_hasil, deskripsi_hasil, total_skor, tanggal FROM hasil_tes WHERE id_user = %s AND jenis_tes = %s ORDER BY tanggal DESC LIMIT 1",
                (session['user_id'], jenis)
            )
            hasil = cursor.fetchone()
            
            if hasil:
                judul = hasil['kategori_hasil']
                deskripsi = hasil['deskripsi_hasil']
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    
    return render_template('hasil.html', nama=nama, judul=judul, deskripsi=deskripsi, jenis=jenis)

# --- ROUTE LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    flash('Kamu telah keluar.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)