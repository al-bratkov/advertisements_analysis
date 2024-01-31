import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats



def check_normality_vis(row):
    plt.figure(figsize=[6.4 * 2, 4.8])
    # draw QQ-plot
    plt.subplot(1, 2, 1)
    stats.probplot(row, dist="norm", plot=plt)
    plt.title('QQ-plot / Квантиль-квантиль')
    plt.xlabel('Квантили Z-распределения')
    plt.ylabel('Квантили фактического распределения')
    plt.grid(True)

    # draw histogram
    plt.subplot(1, 2, 2)
    plt.hist(row, 30, density=True, facecolor='g', alpha=0.75, label='Гистограмма')
    plt.title('Гистограмма распределения')
    plt.xlabel('Промежутки наблюдений')
    plt.ylabel('Плотность наблюдений')
    plt.text(-3, 0.35, r'$\mu=0,\ \sigma=1$')
    plt.grid(True)

    # draw z-plot for comparing with our distributions
    mean = row.mean()
    sd = row.std()
    x = np.linspace(mean - 3 * sd, mean + 3 * sd, 1000)
    plt.plot(x, stats.norm.pdf(x, mean, sd), color='red', label='Z-распределение')

    plt.legend()
    plt.show()

def is_normal(row):
    # furmulas from book by Kurihara Sinity
    asymmetry = (((row - row.mean()) / row.std()) ** 3).sum() / len(row)
    excess = (((row - row.mean()) / row.std()) ** 4).sum() / len(row) - 3

    test_norm = stats.shapiro(row)
    check_normality_vis(row)
    print("=" * 25)
    print(f"||pvalue|| asym || excs ||")
    print("_" * 25)
    print(f"|| {round(test_norm.pvalue, 2)} || {round(asymmetry, 2)} || {round(excess, 2)} ||")
    print("=" * 25)
    return test_norm.pvalue >= 0.05


def check_interview(df, pop_data):
    # https://rg.ru/2023/05/23/sredniaia-cena-otechestvennogo-avtomobilia-s-probegom-sostavliaet-400-tysiach-rublej.html
    sample_data = {"mean_price": 400000, "mean_age": 14, "weighted_avg_mileage": 140000,
           "price_distr": {"<300": 0.53, "300-500": 0.16, "500-800": 0.15, "800-1500": 0.15},
           "age_distr": {">20": 0.25, "15-19": 0.21, "10-14": 0.21, "5-10": 0.12, "3-5": 0.14, "<2": 0.07}}

    df_pas = df[~(df["body_type"].isin(['Микроавтобус', 'Фургон', 'Минивэн', 'Пикап']) & (df["brand"].isin(["ГАЗ", "УАЗ"]))) |
             ~((df["brand"].isin(["ГАЗ", "УАЗ"])) & (~df["model"].isin(["Карго", "Pickup"])))]

    sample_data["mean_price"] = df["price"].mean()
    sample_data["mean_age"] = (2023 - df["car_year"]).mean()
    sample_data["price_distr"] = {}
    price_dist = pd.cut(df["price"], [0, 300_000, 500_000, 800_000, 1_500_000]).value_counts(sort=False, normalize=True)
    sample_data["price_distr"] = {k: v for k, v in zip(pop_data["price_distr"].keys(), price_dist.values)}
    age_dist = pd.cut((2023 - df["car_year"]), [0, 2, 5, 10, 14, 19, 200], include_lowest=True).value_counts(sort=False, normalize=True)[::-1]
    sample_data["age_distr"] = {k: v for k, v in zip(pop_data["age_distr"].keys(), age_dist.values)}

    res = stats.ttest_1samp(df["mileage"], 140000)
    p = round(1 - res[1], 4)


def brand_mileage(df, brand1, brand2):
    cars1 = df[df["brand"] == brand1]["mileage"] / (2024 - df[df["brand"] == brand1]["car_year"])
    cars2 = df[df["brand"] == brand2]["mileage"] / (2024 - df[df["brand"] == brand2]["car_year"])
    # need to check vars
    res = stats.ttest_ind(cars1, cars2, equal_var=True)


def body_mileagee_anova(df):
    u = df[df["body_type"] == 'Универсал']["mileage"]
    s = df[df["body_type"] == 'Седан']["mileage"]
    m = df[df["body_type"] == 'Микроавтобус']["mileage"]
    h = df[df["body_type"] == 'Хетчбэк']["mileage"]
    o = df[df["body_type"] == 'Внедорожник']["mileage"]
    f = df[df["body_type"] == 'Фургон']["mileage"]
    l = df[df["body_type"] == 'Лифтбек']["mileage"]
    p = df[df["body_type"] == 'Пикап']["mileage"]
    mv = df[df["body_type"] == 'Минивэн']["mileage"]
    res = stats.f_oneway(u, s, m, h, o, f, l, p, mv)



rg_data = {"mean_price": 400000, "mean_age": 14, "weighted_avg_mileage": 140000,
           "price_distr": {"<300": 0.53, "300-500": 0.16, "500-800": 0.15, "800-1500": 0.15},
           "age_distr": {">20": 0.25, "15-19": 0.21, "10-14": 0.21, "5-10": 0.12, "3-5": 0.14, "<2": 0.07}}