"""
Delta Challenge 1 — Autograder Tests
Tests run automatically on every push via GitHub Actions
"""
import pytest
import pandas as pd
import os
import json
import nbformat

# ── Helper: load the notebook ──────────────────────────────────────────────
def load_notebook():
    with open('delta_challenge_1.ipynb', 'r', encoding='utf-8') as f:
        return nbformat.read(f, as_version=4)

def get_cell_outputs(nb, cell_index):
    cell = nb.cells[cell_index]
    return ''.join([o.get('text', '') for o in cell.get('outputs', [])])

def get_cell_source(nb, cell_index):
    return nb.cells[cell_index]['source']

# ── Test 1: Data loads correctly ───────────────────────────────────────────
def test_data_file_exists():
    """البيانات موجودة | Data file exists"""
    assert os.path.exists('data/arabic_internet_growth.csv'), \
        "❌ ملف البيانات غير موجود | Data file not found"

def test_data_loads():
    """البيانات تُحمّل بشكل صحيح | Data loads correctly"""
    df = pd.read_csv('data/arabic_internet_growth.csv')
    assert len(df) == 10, "❌ عدد الصفوف غير صحيح | Incorrect number of rows"
    assert 'language' in df.columns, "❌ عمود اللغة غير موجود | Language column missing"
    assert 'growth_pct' in df.columns, "❌ عمود النمو غير موجود | Growth column missing"
    assert 'ai_training_data_pct' in df.columns, "❌ عمود الذكاء الاصطناعي غير موجود | AI column missing"

# ── Test 2: Arabic is in the data ─────────────────────────────────────────
def test_arabic_exists_in_data():
    """العربية موجودة في البيانات | Arabic exists in the data"""
    df = pd.read_csv('data/arabic_internet_growth.csv')
    assert 'Arabic' in df['language'].values, \
        "❌ بيانات العربية غير موجودة | Arabic data not found"

def test_arabic_growth_correct():
    """نمو العربية صحيح | Arabic growth is correct"""
    df = pd.read_csv('data/arabic_internet_growth.csv')
    arabic = df[df['language'] == 'Arabic']
    assert arabic['growth_pct'].values[0] == 9000, \
        "❌ نسبة نمو العربية غير صحيحة | Arabic growth percentage incorrect"

# ── Test 3: Sorting works ─────────────────────────────────────────────────
def test_sorting_produces_arabic_first():
    """العربية تظهر في أعلى القائمة عند الترتيب | Arabic appears at top when sorted"""
    df = pd.read_csv('data/arabic_internet_growth.csv')
    sorted_df = df.sort_values('growth_pct', ascending=False)
    top_language = sorted_df.iloc[0]['language']
    assert top_language == 'Arabic', \
        f"❌ اللغة الأولى يجب أن تكون العربية | First language should be Arabic, got {top_language}"

# ── Test 4: Filtering works ───────────────────────────────────────────────
def test_filtering_arabic():
    """فلترة العربية تعمل | Filtering Arabic works"""
    df = pd.read_csv('data/arabic_internet_growth.csv')
    arabic_data = df[df['language'] == 'Arabic']
    assert len(arabic_data) == 1, \
        "❌ فلترة العربية لا تعمل | Arabic filtering not working"

def test_gap_ratio_calculated():
    """نسبة الفجوة تُحسب بشكل صحيح | Gap ratio calculated correctly"""
    df = pd.read_csv('data/arabic_internet_growth.csv')
    df['gap_ratio'] = df['growth_pct'] / df['ai_training_data_pct']
    arabic_gap = df[df['language'] == 'Arabic']['gap_ratio'].values[0]
    assert arabic_gap > 1000, \
        "❌ نسبة فجوة العربية يجب أن تكون أكبر من 1000 | Arabic gap ratio should be > 1000"

# ── Test 5: Chart was saved ───────────────────────────────────────────────
def test_chart_saved():
    """الرسم البياني محفوظ | Chart was saved"""
    assert os.path.exists('my_finding.png'), \
        "❌ الرسم البياني غير محفوظ — تأكد من تشغيل خلية الرسم | Chart not saved — make sure to run the chart cell"

# ── Test 6: Finding was written ───────────────────────────────────────────
def test_finding_written():
    """الاكتشاف مكتوب | Finding was written"""
    nb = load_notebook()
    # Find the finding cell (cell 7)
    finding_cell = nb.cells[7]['source']
    assert 'اكتشفت أن: ...' not in finding_cell or \
           'I found that: ...' not in finding_cell, \
        "❌ لم تكتب اكتشافك بعد | You haven't written your finding yet — replace the placeholder text"

# ── Test 7: README exists and is bilingual ────────────────────────────────
def test_readme_exists():
    """README موجود | README exists"""
    assert os.path.exists('README.md'), \
        "❌ ملف README غير موجود | README file not found"

def test_readme_bilingual():
    """README ثنائي اللغة | README is bilingual"""
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    assert len(content) > 200, \
        "❌ README قصير جداً — أضف المزيد من المحتوى | README too short — add more content"
    # Check for both Arabic and English content
    has_arabic = any('\u0600' <= c <= '\u06FF' for c in content)
    has_english = any('a' <= c.lower() <= 'z' for c in content)
    assert has_arabic, "❌ README يجب أن يحتوي على محتوى عربي | README must contain Arabic content"
    assert has_english, "❌ README يجب أن يحتوي على محتوى إنجليزي | README must contain English content"
