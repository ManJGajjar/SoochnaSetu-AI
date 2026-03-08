# 🧪 Testing Guide - Scheme Matching Accuracy

## How to Test Accurate Scheme Matching

### Test 1: Student Occupation ✅

**Steps:**
1. Go to `/schemes` page
2. Fill Step 1: Age = 20, Gender = Any, State = Any, District = Any
3. Fill Step 2: Select "Student" occupation only
4. Fill Step 3: Any category
5. Fill Step 4: Select "🎓 Education/Scholarship"
6. Click "Find My Schemes"

**Expected Result:**
Should show ONLY these 3 schemes:
- ✅ NSP Scholarship (₹10,000-50,000/year)
- ✅ Post Matric Scholarship (₹1,000-3,000/month) - if SC/ST/OBC selected
- ✅ Merit-cum-Means Scholarship (₹20,000/year)

**Should NOT show:**
- ❌ PM-KISAN (farmer scheme)
- ❌ MUDRA Loan (business scheme)
- ❌ MGNREGA (employment scheme)

---

### Test 2: Farmer Occupation ✅

**Steps:**
1. Go to `/schemes` page
2. Fill Step 1: Age = 35, Gender = Male
3. Fill Step 2: Select "Farmer" occupation only
4. Fill Step 3: Any category
5. Fill Step 4: Select "🌾 Agricultural Support"
6. Click "Find My Schemes"

**Expected Result:**
Should show ONLY:
- ✅ PM-KISAN (₹6,000/year for farmers)
- ✅ Ayushman Bharat (available for all)
- ✅ PM Awas Yojana (available for all)

**Should NOT show:**
- ❌ NSP Scholarship (student scheme)
- ❌ MUDRA Loan (business scheme)

---

### Test 3: Unemployed Occupation ✅

**Steps:**
1. Go to `/schemes` page
2. Fill Step 1: Age = 25, Gender = Any
3. Fill Step 2: Select "Unemployed" occupation only
4. Fill Step 3: Any category
5. Fill Step 4: Select "💼 Employment/Skill Training"
6. Click "Find My Schemes"

**Expected Result:**
Should show ONLY:
- ✅ MGNREGA (100 days employment)
- ✅ PMEGP (₹25-50 lakh for enterprises)
- ✅ Atal Pension Yojana (pension scheme)
- ✅ Ayushman Bharat (available for all)
- ✅ PM Awas Yojana (available for all)

**Should NOT show:**
- ❌ PM-KISAN (farmer scheme)
- ❌ NSP Scholarship (student scheme)

---

### Test 4: Small Business Owner ✅

**Steps:**
1. Go to `/schemes` page
2. Fill Step 1: Age = 30, Gender = Any
3. Fill Step 2: Select "Small Business Owner" occupation
4. Fill Step 3: Any category
5. Fill Step 4: Select "💰 Financial Assistance"
6. Click "Find My Schemes"

**Expected Result:**
Should show ONLY:
- ✅ MUDRA Loan (Up to ₹10 lakh)
- ✅ Stand-Up India (₹10L-₹1Cr) - if SC/ST/Women
- ✅ Ayushman Bharat (available for all)
- ✅ PM Awas Yojana (available for all)

**Should NOT show:**
- ❌ PM-KISAN (farmer scheme)
- ❌ NSP Scholarship (student scheme)
- ❌ MGNREGA (employment scheme)

---

### Test 5: Multiple Occupations ✅

**Steps:**
1. Go to `/schemes` page
2. Fill Step 1: Age = 22, Gender = Female
3. Fill Step 2: Select BOTH "Student" AND "Unemployed"
4. Fill Step 3: Category = SC
5. Fill Step 4: Select multiple needs
6. Click "Find My Schemes"

**Expected Result:**
Should show schemes from BOTH categories:
- ✅ NSP Scholarship (student)
- ✅ Post Matric Scholarship (student + SC)
- ✅ Merit Scholarship (student)
- ✅ MGNREGA (unemployed)
- ✅ PMEGP (unemployed)
- ✅ Atal Pension (unemployed)
- ✅ Ayushman Bharat (all)
- ✅ PM Awas Yojana (all)

---

### Test 6: Age Filtering ✅

**Test 6a: Child (Age 8)**
- Should show: Sukanya Samriddhi (if female, age ≤10)
- Should NOT show: MGNREGA (requires age ≥18)

**Test 6b: Senior (Age 45)**
- Should NOT show: NSP Scholarship (max age 30)
- Should NOT show: Atal Pension (max age 40)

---

### Test 7: Gender Filtering ✅

**Steps:**
1. Age = 8, Gender = Female
2. Should show: Sukanya Samriddhi Yojana (girl child scheme)

**Steps:**
1. Age = 8, Gender = Male
2. Should NOT show: Sukanya Samriddhi Yojana

---

### Test 8: Category Filtering ✅

**Steps:**
1. Age = 20, Occupation = Student, Category = SC
2. Should show: Post Matric Scholarship (SC/ST/OBC only)

**Steps:**
1. Age = 20, Occupation = Student, Category = General
2. Should NOT show: Post Matric Scholarship

---

## 🎨 Testing UI Features

### Landing Page
- ✅ Animated background blobs floating
- ✅ Glassmorphism effects on cards
- ✅ Smooth scroll animations
- ✅ Gradient text effects
- ✅ Hover effects on buttons
- ✅ Responsive on mobile

### Voice Assistant
- ✅ Language toggle works (EN/HI)
- ✅ Microphone button changes color when listening
- ✅ Sound wave animation appears
- ✅ Transcript displays after listening
- ✅ AI response appears with delay
- ✅ Quick question buttons work
- ✅ Glassmorphism background

### Document Explainer
- ✅ Drag & drop area highlights on drag
- ✅ File input works
- ✅ Example documents are clickable
- ✅ Processing animation shows
- ✅ Explanation view displays correctly
- ✅ All action buttons present
- ✅ Glassmorphism effects

### Scheme Finder
- ✅ Progress bar updates with each step
- ✅ Multi-select occupation works
- ✅ Multi-select needs works
- ✅ Loading animation shows
- ✅ Results display with correct schemes
- ✅ Match percentage shows
- ✅ Confidence score displays
- ✅ Apply Now links work
- ✅ Helpline numbers visible

---

## 🐛 Common Issues & Solutions

### Issue: Schemes not filtering correctly
**Check:**
- Occupation is selected in Step 2
- Age is filled in Step 1
- Wait for loading animation to complete

### Issue: No schemes showing
**Possible reasons:**
- Age too young/old for available schemes
- Occupation doesn't match any schemes
- Try selecting multiple occupations

### Issue: Too many schemes showing
**This is correct if:**
- Multiple occupations selected
- Schemes marked as "all" occupations (Ayushman Bharat, PM Awas)

---

## ✅ Verification Checklist

Before considering testing complete, verify:

- [ ] Student sees ONLY student schemes
- [ ] Farmer sees ONLY farmer schemes
- [ ] Unemployed sees ONLY employment schemes
- [ ] Business owner sees ONLY business schemes
- [ ] Multiple occupations show combined results
- [ ] Age filtering works correctly
- [ ] Gender filtering works (Sukanya Samriddhi)
- [ ] Category filtering works (Post Matric)
- [ ] All 12 schemes are in the database
- [ ] No TypeScript errors in console
- [ ] All pages load without errors
- [ ] Animations are smooth
- [ ] Mobile responsive works
- [ ] All buttons are clickable
- [ ] All links work

---

## 📊 Expected Scheme Distribution

**By Occupation:**
- Student: 3 schemes
- Farmer: 1 scheme (+ 2 "all")
- Unemployed: 3 schemes (+ 2 "all")
- Business Owner: 2 schemes (+ 2 "all")
- Self-Employed: 3 schemes (+ 2 "all")
- Daily Wage Worker: 2 schemes (+ 2 "all")
- All Occupations: 2 schemes (Ayushman, PM Awas)

**Total Unique Schemes:** 12

---

**Testing Complete!** ✅

If all tests pass, the scheme matching is 100% accurate and the platform is ready for production use.
