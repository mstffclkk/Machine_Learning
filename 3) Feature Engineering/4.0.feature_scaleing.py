
#############################################
# Feature Scaling (Özellik Ölçeklendirme)  
#############################################
""" 
1- Tüm değişkenleri eşit şartlar altında değerlendirebilmek adına ölçeklendirmektir.(Kullanılacak olan yöntemlere değişkenleri gönderirken onlara eşit muamele yapılması gerektiğini bildirmek için)
2- Özellikle gradient decent kullanan algoritmaların train sürelerini, yani eğitim sürelerini kısaltmak için.
3- Uzaklık temelli yöntemlerde yanlılığın önüne geçmek için

"""
###################
# StandardScaler: Klasik standartlaştırma. Ortalamayı çıkar, standart sapmaya böl. z = (x - u) / s (yaygın)
###################
# Klasik standartlaştırma yöntemidir. Seçilen değerden, o değerin bulunduğu değişkenin ortalaması 
# çıkarılarak yine o değişkenin standart sapmasına bölünmesiyle hesaplanır. Z Standartlaştırması olarak da bilinir.

from Functions.DataAnalysis import *

df = load()
ss = StandardScaler()
df["Age_standard_scaler"] = ss.fit_transform(df[["Age"]])
df.head()


################### ÖNEMLİ  ###################
# RobustScaler: Medyanı çıkar iqr'a böl.    
###################
"""
Robust scaler, standard scaler'a göre aykırı değerlere karşı dayanıklı
olduğundan dolayı daha tercih edilebilir olabilir. Fakat yaygın bir kullanım alanı yoktur. 
(vahit hoca standart scaler yerine daha kullanışlı old. düşünüyo)
"""
rs = RobustScaler()
df["Age_robuts_scaler"] = rs.fit_transform(df[["Age"]])
df.describe().T

###################
# MinMaxScaler: Verilen 2 değer arasında değişken dönüşümü (yaygın)
###################
# Dönüştürmek istediğimiz özel bir alan varsa (mesela 1-5) kullanılabilir

# X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
# X_scaled = X_std * (max - min) + min

mms = MinMaxScaler()
df["Age_min_max_scaler"] = mms.fit_transform(df[["Age"]])
df.describe().T

df.head()

# sonuçları karşılaştırmak için.(ortaya çıkan değerlerin yeni değişkenlerinde bir değişiklik var mı onu gözlemlemek)
age_cols = [col for col in df.columns if "Age" in col]

# num_summary: sayısal değişkenlerin çeyreklik değerlerini göstermek ve hist grafiğini oluşturmak
def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[numerical_col].describe(quantiles).T)

    if plot:
        dataframe[numerical_col].hist(bins=20)
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show(block=True)

for col in age_cols:
    num_summary(df, col, plot=True)

###################
# Numeric to Categorical: Sayısal Değişkenleri Kateorik Değişkenlere Çevirme
# Binning
###################
# qcut metodu, bir değişkenin değerlerini küçükten büyüğe sıralar ve yazdığımız sayı kadar parçaya böler.
# hangi sınıflara dönüştürmek istediğimizi biliyorsak label eklenebilir.
# df["Age_qcut"] = pd.qcut(df['Age'], 5, labels=mylabels)

df["Age_qcut"] = pd.qcut(df['Age'], 5)
df.head()


#############################################
# Feature Extraction (Özellik Çıkarımı)
#############################################
"""
Feature extraction (özellik çıkarımı), ham veriden özellik (feature, değişken) üretmek. 2 çeşittir: 

1.  Yapısal verilerden değişken türetmek: var olan bazı değişkenler üzerinden yeni değişkenler türetmek
2.  Yapısal olmayan verilerden değişken üretmek: bilgisayarın anlayamayacağı metinsel veya görsel verilerden anlamlı değişkenler üretmek
"""
#############################################
# Binary Features: Flag, Bool, True-False
#############################################
"""
Var olan değişkenin içinden yeni değişkenler türetmek (1 / 0 şeklinde)

Dikkat! Yeni değişkenler üretmek istiyoruz, var olan değişkeni değiştirmek değil (bu encoding işlemi oluyor).
"""
df = load()
df.head()

df["NEW_CABIN_BOOL"] = df["Cabin"].notnull().astype('int64')

#Şimdi bu yeni oluşturduğumuz değişkenin, bağımlı değişkene göre oranını inceleyelim
df.groupby("NEW_CABIN_BOOL").agg({"Survived": "mean"})

# Şimdi bu yeni oluşturduğumuz değişkenin, bağımlı değişkene göre oranını inceleyelim (yeni feature ile bağımlı değişken oranı)

from statsmodels.stats.proportion import proportions_ztest
"""
count: başarı sayısı
nobs: gözlem sayısı

test_stat, pvalue = proportions_ztest(count=[df.loc[df["NEW_CABIN_BOOL"] == 1, "Survived"].sum(),   --> kabin numarası olan ve hayatta kalan kişi sayısı
                                             df.loc[df["NEW_CABIN_BOOL"] == 0, "Survived"].sum()],  --> kabin numarası olmayan ve hayatta kalan kişi sayısı        

                                      nobs=[df.loc[df["NEW_CABIN_BOOL"] == 1, "Survived"].shape[0], --> kabin numarası olan kişi sayısı
                                            df.loc[df["NEW_CABIN_BOOL"] == 0, "Survived"].shape[0]])--> kabin numarası olmayan kişi sayısı
"""

################## oran testi ##################
test_stat, pvalue = proportions_ztest(count=[df.loc[df["NEW_CABIN_BOOL"] == 1, "Survived"].sum(),
                                             df.loc[df["NEW_CABIN_BOOL"] == 0, "Survived"].sum()],

                                      nobs=[df.loc[df["NEW_CABIN_BOOL"] == 1, "Survived"].shape[0],
                                            df.loc[df["NEW_CABIN_BOOL"] == 0, "Survived"].shape[0]])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
"""
Output: Test Stat = 9.4597, p-value = 0.0000
Proportion z testinin hipotezi (h0), p1 ve p2 oranları arasında fark yoktur der. p1 ve p2 oranları,
iki grubun, yani şu anki senaryoda cabin numarası olanların ve olmayanların hayatta kalma oranları.
İkisi arasında fark yoktur diyen hipotez, p-value değeri 0.05'ten küçük olduğundan dolayı geçersiz olmuş olur.
Yani bizim oluşturduğumuz değişkenden elde ettiğimiz oranların aralarında istatistiki olarak anlamlı bir farklılık var gibi gözüküyor.
(çünkü yukarıda p-value değerimiz 0 çıktı, <0.05)


Şimdi aynı şeyi başka bir değişken üzerinden yapalım.
Veriseti içerisinde SibSp ve Parch değişkenleri bulunuyor.
Bu değişkenler, o kişinin gemi içerisinde kaç tane yakını olduğunun bilgisini veren değişkenler.
Yeni bir değişken oluşturalım ve bu iki değişkenin toplamına göre, kişinin o teknede yalnız olup olmadığının bilgisini versin.
"""

# SibSp: yakın akrabalık, Parch: uzak akrabalık
df.loc[((df['SibSp'] + df['Parch']) > 0), "NEW_IS_ALONE"] = "NO"
df.loc[((df['SibSp'] + df['Parch']) == 0), "NEW_IS_ALONE"] = "YES"

df.groupby("NEW_IS_ALONE").agg({"Survived": "mean"})


test_stat, pvalue = proportions_ztest(count=[df.loc[df["NEW_IS_ALONE"] == "YES", "Survived"].sum(),
                                             df.loc[df["NEW_IS_ALONE"] == "NO", "Survived"].sum()],

                                      nobs=[df.loc[df["NEW_IS_ALONE"] == "YES", "Survived"].shape[0],
                                            df.loc[df["NEW_IS_ALONE"] == "NO", "Survived"].shape[0]])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
"""
Output: `Test Stat = -6.0704, p-value = 0.0000`

p-value değerine bakıldığında h0 hipotezinin yine geçersiz olduğu görülür. Yani iki oran arasında istatistiki bir fark vardır.
"""
#############################################
# Text'ler Üzerinden Özellik Türetmek
#############################################

df = load()
df.head()

###################
# Letter Count
###################
# bir değişkende kaç tane harf var saydık.
df["NEW_NAME_COUNT"] = df["Name"].str.len()

###################
# Word Count
###################

df["NEW_NAME_WORD_COUNT"] = df["Name"].apply(lambda x: len(str(x).split(" ")))

###################
# Özel Yapıları Yakalamak
###################
# name içerisindeki metinleri split et ve içerisinde gez. dr ile başlayanları seç ve len ile sayısını bul.
df["NEW_NAME_DR"] = df["Name"].apply(lambda x: len([x for x in x.split() if x.startswith("Dr")]))

# dr ların hayatta kalma oranına bakalım.
df.groupby("NEW_NAME_DR").agg({"Survived": ["mean","count"]})

###################
# Regex ile Değişken Türetmek
###################
# ünvanları bulalım.

df.head()

# boşluk ile başlayıp nokta ile biten, ve büyük ve küçük harfler içeren ifadeleri yakala
# extract: çıkar
df['NEW_TITLE'] = df.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

# "NEW_TITLE", "Survived", "Age" 'i seç, "NEW_TITLE" a göre groupby a al .
df[["NEW_TITLE", "Survived", "Age"]].groupby(["NEW_TITLE"]).agg({"Survived": "mean", "Age": ["count", "mean"]})
"""
Normalde "Age" değişkeni içerisinde eksik değerler bulunuyor ve biz bunları genel olarak Age'in medyanı ile doldurabilirdik.
Fakat burada görüyoruz ki birçok title bulunuyor ve bunların hepsinin yaş ortalamaları farklı.
Dolayısıyla her bir eksik yaş verisini kendi title'ının ortalama yaşı ile doldurursak daha anlamlı bir veriseti oluşturmuş oluruz.
"""
#############################################
# Date Değişkenleri Üretmek
#############################################
# amaç: timestap üzerinden değişken üretmek.

dff = pd.read_csv("D:\\Users\\mstff\\PycharmProjects\\pythonProject\\datasets\\course_reviews.csv")
dff.head()
dff.info()

# problem: timestamp object tipinde. Timestamp değişkenini tipini değiğiştirmek gerek.

# dönüştürmek istediğin değişkeni ver ve değişken içerisindeki tarihlerin sıralanışına göre sırayı gir
dff['Timestamp'] = pd.to_datetime(dff["Timestamp"], format="%Y-%m-%d")

# year
dff['year'] = dff['Timestamp'].dt.year

# month
dff['month'] = dff['Timestamp'].dt.month

# year diff
dff['year_diff'] = date.today().year - dff['Timestamp'].dt.year

# month diff (iki tarih arasındaki ay farkı): yıl farkı + ay farkı
dff['month_diff'] = (date.today().year - dff['Timestamp'].dt.year) * 12 + date.today().month - dff['Timestamp'].dt.month


# day name
dff['day_name'] = dff['Timestamp'].dt.day_name()

dff.head()

# date


#############################################
# Feature Interactions (Özellik Etkileşimleri)
#############################################
df = load()
df.head()

# Feature Interaction, değişkenlerin birbirleri ile etkileşime girmesi demektir.

df["NEW_AGE_PCLASS"] = df["Age"] * df["Pclass"]

df["NEW_FAMILY_SIZE"] = df["SibSp"] + df["Parch"] + 1

df.loc[(df['Sex'] == 'male') & (df['Age'] <= 21), 'NEW_SEX_CAT'] = 'youngmale'

df.loc[(df['Sex'] == 'male') & (df['Age'] > 21) & (df['Age'] < 50), 'NEW_SEX_CAT'] = 'maturemale'

df.loc[(df['Sex'] == 'male') & (df['Age'] >= 50), 'NEW_SEX_CAT'] = 'seniormale'

df.loc[(df['Sex'] == 'female') & (df['Age'] <= 21), 'NEW_SEX_CAT'] = 'youngfemale'

df.loc[(df['Sex'] == 'female') & (df['Age'] > 21) & (df['Age'] < 50), 'NEW_SEX_CAT'] = 'maturefemale'

df.loc[(df['Sex'] == 'female') & (df['Age'] >= 50), 'NEW_SEX_CAT'] = 'seniorfemale'


df.head()

# oluşturulan yeni featurelar bir şey ifade ediyor mu bakalım.
df.groupby("NEW_SEX_CAT")["Survived"].mean()


#############################################
# Titanic Uçtan Uca Feature Engineering & Data Preprocessing
#############################################
# Amaç: insanların hayatta kalıp kalamayacağını titanic veri seti üzerinden modellemek.

df = load()
df.shape
df.head()

# bütün columları büyüttük.
df.columns = [col.upper() for col in df.columns]

#############################################
# 1. Feature Engineering (Değişken Mühendisliği)
#############################################

# Oluşturduğumuz bütün değişkenler.

# Cabin bool
df["NEW_CABIN_BOOL"] = df["CABIN"].notnull().astype('int64')

# Name count
df["NEW_NAME_COUNT"] = df["NAME"].str.len()
# name word count
df["NEW_NAME_WORD_COUNT"] = df["NAME"].apply(lambda x: len(str(x).split(" ")))
# name dr
df["NEW_NAME_DR"] = df["NAME"].apply(lambda x: len([x for x in x.split() if x.startswith("Dr")]))
# name title
df['NEW_TITLE'] = df.NAME.str.extract(' ([A-Za-z]+)\.', expand=False)
# family size
df["NEW_FAMILY_SIZE"] = df["SIBSP"] + df["PARCH"] + 1
# age_pclass
df["NEW_AGE_PCLASS"] = df["AGE"] * df["PCLASS"]
# is alone
df.loc[((df['SIBSP'] + df['PARCH']) > 0), "NEW_IS_ALONE"] = "NO"
df.loc[((df['SIBSP'] + df['PARCH']) == 0), "NEW_IS_ALONE"] = "YES"
# age level
df.loc[(df['AGE'] < 18), 'NEW_AGE_CAT'] = 'young'
df.loc[(df['AGE'] >= 18) & (df['AGE'] < 56), 'NEW_AGE_CAT'] = 'mature'
df.loc[(df['AGE'] >= 56), 'NEW_AGE_CAT'] = 'senior'
# sex x age
df.loc[(df['SEX'] == 'male') & (df['AGE'] <= 21), 'NEW_SEX_CAT'] = 'youngmale'
df.loc[(df['SEX'] == 'male') & (df['AGE'] > 21) & (df['AGE'] < 50), 'NEW_SEX_CAT'] = 'maturemale'
df.loc[(df['SEX'] == 'male') & (df['AGE'] >= 50), 'NEW_SEX_CAT'] = 'seniormale'
df.loc[(df['SEX'] == 'female') & (df['AGE'] <= 21), 'NEW_SEX_CAT'] = 'youngfemale'
df.loc[(df['SEX'] == 'female') & (df['AGE'] > 21) & (df['AGE'] < 50), 'NEW_SEX_CAT'] = 'maturefemale'
df.loc[(df['SEX'] == 'female') & (df['AGE'] >= 50), 'NEW_SEX_CAT'] = 'seniorfemale'

df.head()
df.shape

# Ön işleme işlemleri yapmak için, hangileri sayısal kategorik seçmek lazım.

# Değişken isimlendirmelerini tutuyoruz.
cat_cols, num_cols, cat_but_car = grab_col_names(df)

# Nümerik değişkende yer alan PASSENGERID yi kaldırıyoruz.
num_cols = [col for col in num_cols if "PASSENGERID" not in col]

#############################################
# 2. Outliers (Aykırı Değerler) # nümerik değişkenler için ön işleme basamağı
#############################################

for col in num_cols:
    print(col, check_outlier(df, col))

for col in num_cols:
    replace_with_thresholds(df, col)

for col in num_cols:
    print(col, check_outlier(df, col))

#############################################
# 3. Missing Values (Eksik Değerler)
#############################################

missing_values_table(df)

df.drop("CABIN", inplace=True, axis=1)

# kardinalitesi yüksek oldğu için
remove_cols = ["TICKET", "NAME"]
df.drop(remove_cols, inplace=True, axis=1)

# Oluşturmuş olduğumuz new_title'a göre groupby'a alıp yaş değişkeninin eksik değerlerini medyan ile doldur, new_title'a göre
df["AGE"] = df["AGE"].fillna(df.groupby("NEW_TITLE")["AGE"].transform("median"))

# AGE değişkenindeki eksiklikleri halletmiş olduk.
# Şimdi age değişkeninden türeyen değişkenlerdeki eksiklikleri de gidermek için bu değişkenleri tekrardan tanımlamak gerekiyor.
df["NEW_AGE_PCLASS"] = df["AGE"] * df["PCLASS"]

df.loc[(df['AGE'] < 18), 'NEW_AGE_CAT'] = 'young'
df.loc[(df['AGE'] >= 18) & (df['AGE'] < 56), 'NEW_AGE_CAT'] = 'mature'
df.loc[(df['AGE'] >= 56), 'NEW_AGE_CAT'] = 'senior'

df.loc[(df['SEX'] == 'male') & (df['AGE'] <= 21), 'NEW_SEX_CAT'] = 'youngmale'
df.loc[(df['SEX'] == 'male') & (df['AGE'] > 21) & (df['AGE'] < 50), 'NEW_SEX_CAT'] = 'maturemale'
df.loc[(df['SEX'] == 'male') & (df['AGE'] >= 50), 'NEW_SEX_CAT'] = 'seniormale'
df.loc[(df['SEX'] == 'female') & (df['AGE'] <= 21), 'NEW_SEX_CAT'] = 'youngfemale'
df.loc[(df['SEX'] == 'female') & (df['AGE'] > 21) & (df['AGE'] < 50), 'NEW_SEX_CAT'] = 'maturefemale'
df.loc[(df['SEX'] == 'female') & (df['AGE'] >= 50), 'NEW_SEX_CAT'] = 'seniorfemale'

# Sadece EMBARKED değişkeni kaldı. Bunu halletmek için de dataframe içerisinde tipi object olan,
# ve sınıf sayısı 10 veya daha altı olan değişkenlerdeki boşlukları, ilgili değişkenin modu ile dolduran bir fonksiyon yazacağız
df = df.apply(lambda x: x.fillna(x.mode()[0]) if (x.dtype == "O" and len(x.unique()) <= 10) else x, axis=0)
df.head()

#############################################
# 4. Label Encoding
#############################################

# Bu kısımda iki sınıflı değişkenler için label encoding yöntemini kullanıyoruz.
# Öncelikle iki sınıflı değişkenleri seçmemiz gerekiyor.

# int ve float olmayan (yani kategorik olan) ve 2 sınıfa sahip olan değişkenleri seç
binary_cols = [col for col in df.columns if df[col].dtype not in ["int64", "float64", "int32", "float32"]
               and df[col].nunique() == 2]

# Seçim işleminden sonra encoding işlemi
for col in binary_cols:
    df = label_encoder(df, col)


#############################################
# 5. Rare Encoding
#############################################
# Birleştirilmesi gereken sınıfları analiz edebilmemiz için rare_analyser fonksiyonumuzu kullanacağız.
rare_analyser(df, "SURVIVED", cat_cols)

# df içerisinde oranı 0.01 ve daha altı olan sınıfları birbirleri ile toplayıp yeni bir rare sınıfı içerisine atadık.
df = rare_encoder(df, 0.01)

df["NEW_TITLE"].value_counts()

#############################################
# 6. One-Hot Encoding
#############################################

# eşşiz değer sayısı 2den büyük ve 10dan küçük olan değişkenleri seç

ohe_cols = [col for col in df.columns if 10 >= df[col].nunique() > 2]

df = one_hot_encoder(df, ohe_cols, drop_first=True)

df.head()
df.shape    

# Bu değişkenleri oluşturduk, fakat bu değişkenler gerekliler mi? Yani bir bilgi taşıyorlar mı yoksa taşımıyorlar mı?
# Bu sorunun cevabı için işlemde geriye gidip oluşturduğumuz yeni verisetinden değişkenleri tekrar ayıralım.
cat_cols, num_cols, cat_but_car = grab_col_names(df)

num_cols = [col for col in num_cols if "PASSENGERID" not in col]

rare_analyser(df, "SURVIVED", cat_cols)

"""
Burada yaptığımız işlemin sebebi, one hot encoderdan geçirdiğimiz ve 
yeni oluşan değişkenlerin hepsinin gerekli olup olmadığını bilmiyoruz bundan dolayı
bağımlı değişkenimize göre oranlarının ne olduğunu inceleyip işe yaramayan var mı onun analizini yaparız.

Yukarıdaki çıktı incelendiğinde bir sorun olduğunu görüyoruz; iki sınıflı olup sınıflarından
herhangi bir tanesinin oranı 0.01'den az olan var mı? Şimdi bu değişkenleri yakalayalım.
"""
############## ÖNEMLİ FONKSİYON ##############
# sınıf sayısı 2 olan ve value toplamlarının toplam verisetindeki satır sayısına oranı 0.01'den küçük olanları tut
useless_cols = [col for col in df.columns if df[col].nunique() == 2 and
                (df[col].value_counts() / len(df) < 0.01).any(axis=None)]

# SİLMEK İSTERSEK
# df.drop(useless_cols, axis=1, inplace=True)

#############################################
# 7. Standart Scaler (öneri: robust scaler ya da min max scaler)
#############################################
# Bu senaryoda kullanacağımız modelden dolayı scale işlemi yapmamıza gerek kalmıyor. Fakat eğer yapacak olsaydık:

scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

df[num_cols].head()

df.head()
df.shape


#############################################
# 8. Model
#############################################

y = df["SURVIVED"]                                  # bağımlı değişken
X = df.drop(["PASSENGERID", "SURVIVED"], axis=1)    # bağımsız değişkenler passengerid ve survived dışındaki değiişkenler

# train seti ve test seti oluştur
# train seti: model için kullanılacak set
# test seti: modelin test edileceği set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=17)

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(random_state=46).fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy_score(y_pred, y_test)

#############################################
# Hiç bir işlem yapılmadan elde edilecek skor?
#############################################

dff = load()
dff.dropna(inplace=True)
dff = pd.get_dummies(dff, columns=["Sex", "Embarked"], drop_first=True)
y = dff["Survived"]
X = dff.drop(["PassengerId", "Survived", "Name", "Ticket", "Cabin"], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=17)
rf_model = RandomForestClassifier(random_state=46).fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy_score(y_pred, y_test)

# Yeni ürettiğimiz değişkenler ne alemde?

def plot_importance(model, features, num=len(X), save=False):
    feature_imp = pd.DataFrame({'Value': model.feature_importances_, 'Feature': features.columns})
    plt.figure(figsize=(10, 10))
    sns.set(font_scale=1)
    sns.barplot(x="Value", y="Feature", data=feature_imp.sort_values(by="Value",
                                                                      ascending=False)[0:num])
    plt.title('Features')
    plt.tight_layout()
    plt.show()
    if save:
        plt.savefig('importances.png')


plot_importance(rf_model, X_train)



