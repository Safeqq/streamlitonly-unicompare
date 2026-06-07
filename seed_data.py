import asyncio, os, sys
sys.path.insert(0, os.path.abspath("D:/Kuliah/SMT 4/PBKK/FP/unicompare-be"))
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///D:/Kuliah/SMT 4/PBKK/FP/unicompare-be/unicompare.db"

from app.database import _get_sessionmaker, Base
from app.models import University, Program, Source

DATA = [
    ("ui", "Universitas Indonesia", [("Kedokteran", 750.5), ("Ilmu Hukum", 710.2), ("Ilmu Komputer", 735.8), ("Manajemen", 720.0), ("Akuntansi", 715.4), ("Teknik Industri", 700.1), ("Psikologi", 690.5), ("Ilmu Komunikasi", 685.3)]),
    ("itb", "Institut Teknologi Bandung", [("Sekolah Teknik Elektro dan Informatika (STEI)", 760.0), ("Fakultas Teknik Pertambangan dan Perminyakan (FTTM)", 745.2), ("Sekolah Bisnis dan Manajemen (SBM)", 730.5), ("Fakultas Teknologi Industri (FTI)", 710.4), ("Fakultas Teknik Sipil dan Lingkungan (FTSL)", 705.8), ("Sekolah Arsitektur, Perencanaan dan Pengembangan Kebijakan (SAPPK)", 695.1)]),
    ("ugm", "Universitas Gadjah Mada", [("Kedokteran", 740.0), ("Teknologi Informasi", 725.5), ("Ilmu Hukum", 705.3), ("Manajemen", 712.1), ("Psikologi", 695.0), ("Hubungan Internasional", 690.4), ("Arsitektur", 680.7), ("Ilmu Komunikasi", 675.2)]),
    ("its", "Institut Teknologi Sepuluh Nopember", [("Teknik Informatika", 720.5), ("Sistem Informasi", 700.2), ("Teknik Industri", 690.8), ("Teknik Elektro", 685.1), ("Teknik Sipil", 675.4), ("Arsitektur", 665.0)]),
    ("unair", "Universitas Airlangga", [("Kedokteran", 735.0), ("Kedokteran Gigi", 710.5), ("Ilmu Hukum", 695.2), ("Psikologi", 680.1), ("Kesehatan Masyarakat", 660.8), ("Manajemen", 670.3)]),
    ("undip", "Universitas Diponegoro", [("Kedokteran", 715.4), ("Kesehatan Masyarakat", 645.2), ("Teknik Sipil", 630.0), ("Teknik Mesin", 625.8), ("Ilmu Hukum", 650.5), ("Ilmu Komunikasi", 640.1), ("Informatika", 680.2), ("Akuntansi", 655.7)]),
    ("unpad", "Universitas Padjadjaran", [("Pendidikan Dokter", 720.1), ("Psikologi", 670.5), ("Ilmu Komunikasi", 665.8), ("Ilmu Hukum", 660.4), ("Manajemen", 655.0), ("Akuntansi", 645.3), ("Teknik Informatika", 675.2), ("Hubungan Internasional", 650.0)]),
    ("ub", "Universitas Brawijaya", [("Kedokteran", 718.5), ("Teknik Informatika", 685.0), ("Ilmu Hukum", 640.2), ("Manajemen", 635.8), ("Teknik Industri", 645.5), ("Kesehatan Masyarakat", 620.4), ("Ilmu Komunikasi", 630.1), ("Administrasi Bisnis", 625.6)]),
    ("uns", "Universitas Sebelas Maret", [("Kedokteran", 710.2), ("Informatika", 670.8), ("Teknik Sipil", 625.5), ("Ilmu Hukum", 635.4), ("Manajemen", 630.1), ("Psikologi", 645.0), ("Ilmu Komunikasi", 620.8)]),
    ("unnes", "Universitas Negeri Semarang", [("Pendidikan Guru Sekolah Dasar", 580.5), ("Manajemen", 595.2), ("Akuntansi", 590.1), ("Ilmu Hukum", 605.8), ("Teknik Informatika", 620.4), ("Kesehatan Masyarakat", 585.5), ("Pendidikan Bahasa Inggris", 570.6)]),
    ("upi", "Universitas Pendidikan Indonesia", [("Pendidikan Guru Sekolah Dasar", 590.2), ("Psikologi", 620.5), ("Manajemen", 610.8), ("Ilmu Komunikasi", 605.4), ("Pendidikan Bahasa Inggris", 585.1), ("Ilmu Komputer", 635.7)]),
    ("unhas", "Universitas Hasanuddin", [("Pendidikan Dokter", 705.4), ("Kesehatan Masyarakat", 615.2), ("Teknik Informatika", 655.8), ("Ilmu Hukum", 625.1), ("Manajemen", 620.5), ("Teknik Sipil", 610.4), ("Kehutanan", 580.6)]),
]

async def seed():
    import app.database as dbmod
    dbmod._get_sessionmaker()
    async with dbmod._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    sm = dbmod._get_sessionmaker()
    async with sm() as session:
        session.add(Source(name="internal_mock", label="Prediksi Internal (Mock)", count=45))
        for uid, uname, progs in DATA:
            uni = University(id=uid, name=uname, sources=["internal_mock"])
            session.add(uni)
            for pname, pscore in progs:
                session.add(Program(university_id=uid, name=pname, score_text=str(pscore), degree="S1", score=pscore, source_count=1))
        await session.commit()
    print("Seed selesai!")

asyncio.run(seed())
