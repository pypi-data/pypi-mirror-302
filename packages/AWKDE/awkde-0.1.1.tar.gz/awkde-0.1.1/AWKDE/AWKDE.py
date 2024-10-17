import numpy as np

# تابع W برای روش ML_k
def W_matrix(X, Sigma):
    # ایجاد ماتریس فاصله‌ها
    diff = X[:, np.newaxis] - X[np.newaxis, :]  # فاصله بین تمام نقاط
    return np.exp(-((diff ** 2) / (2 * Sigma ** 2)))  # محاسبه W برای همه نقاط

# تابع ML_k برای انتخاب Sigma
def AWKDE(x, iterations, weights=None):
    N = len(x)
    Maxbandwidth = (np.max(x) - np.min(x))  # محاسبه Maxbandwidth بر اساس بازه داده‌ها
    MinSigma = np.sqrt(Maxbandwidth / N)
    Sigma = np.full(N, Maxbandwidth)  # مقداردهی اولیه Sigma

    # تکرار برای محاسبه Sigma
    for _ in range(iterations):
        SigmaML = np.copy(Sigma)  # برای ذخیره Sigma جدید

        # اگر وزن‌ها مشخص نشده باشند، وزن‌ها را برابر 1 در نظر می‌گیریم
        if weights is None:
            weights = np.ones(N)

        # محاسبه W به صورت ماتریسی
        W_matrix_values = W_matrix(x, Sigma)

        np.fill_diagonal(W_matrix_values, 0)

        M = np.sum(W_matrix_values * weights[np.newaxis, :], axis=1)  # محاسبه M با جمع‌زنی در امتداد سطرها
        M[M == 0] = 1  # جلوگیری از تقسیم بر صفر

        for k in range(N):
            if weights[k] == 0:
                SigmaML[k] = Sigma[k]
            else:
                a = np.sum(((weights[k] * W_matrix_values[k, :]) / M) * (x[k] - x) ** 2)  # محاسبه a
                c = np.sum((weights[k] * W_matrix_values[k, :]) / M)  # محاسبه c

                if (a > 0) and (c != 0) and np.isfinite(a) and np.isfinite(c):
                    SigmaML[k] = np.sqrt(a / c)
                    if SigmaML[k] < MinSigma:
                        SigmaML[k] = MinSigma  # جلوگیری از کاهش Sigma کمتر از حداقل
                else:
                    SigmaML[k] = Sigma[k]  # اگر محاسبه مشکل داشت، Sigma اولیه استفاده می‌شود

        Sigma = SigmaML  # بروزرسانی Sigma
    return Sigma
