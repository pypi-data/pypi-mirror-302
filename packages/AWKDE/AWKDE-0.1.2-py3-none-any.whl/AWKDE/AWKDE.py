import numpy as np


# تابع ML_k برای انتخاب Sigma
def AWKDE(x, iterations, weights=None):
    # تابع W برای روش ML_k
    def W_matrix(X, Sigma):
        # ایجاد ماتریس فاصله‌ها
        diff = X[:, np.newaxis] - X[np.newaxis, :]  # فاصله بین تمام نقاط
        return np.exp(-((diff ** 2) / (2 * Sigma ** 2)))  # محاسبه W برای همه نقاط

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


import numpy as np

# تابع ML_k برای انتخاب Sigma به صورت ماتریس d * d
def AWKDE_d(X, iterations, weights=None):
    N, d = X.shape

    # تابع W برای روش ML_k با استفاده از فاصله ماهالانوبیس
    def W_matrix(X, Sigma):
        W = np.zeros((N, N))
        for i in range(N):
            diff = X - X[i]  # اختلاف بین تمام نقاط و نقطه i
            inv_Sigma = np.linalg.inv(Sigma[i])  # معکوس ماتریس کواریانس
            # محاسبه فاصله ماهالانوبیس
            mahalanobis_dist = np.einsum('ij,jk,ik->i', diff, inv_Sigma, diff)
            W[:, i] = np.exp(-mahalanobis_dist / 2)  # محاسبه W با استفاده از فاصله ماهالانوبیس
        return W

    Maxbandwidth = np.max(np.linalg.norm(X - np.mean(X, axis=0), axis=1))
    MinSigma = np.sqrt(Maxbandwidth / N / (d**2)) * np.eye(d)  # ماتریس همانی برای حداقل Sigma

    # مقداردهی اولیه Sigma به عنوان یک ماتریس d * d برای هر نقطه
    Sigma = np.array([Maxbandwidth * np.eye(d) for _ in range(N)])

    # تکرار برای محاسبه Sigma
    for _ in range(iterations):
        SigmaML = np.copy(Sigma)

        # اگر وزن‌ها مشخص نشده باشند، وزن‌ها را برابر 1 در نظر می‌گیریم
        if weights is None:
            weights = np.ones(N)

        # محاسبه W به صورت ماتریسی با استفاده از فاصله ماهالانوبیس
        W_matrix_values = W_matrix(X, Sigma)
        np.fill_diagonal(W_matrix_values, 0)

        M = np.sum(W_matrix_values * weights[np.newaxis, :], axis=1)  # محاسبه M با جمع‌زنی در امتداد سطرها
        M[M == 0] = 1  # جلوگیری از تقسیم بر صفر

        for k in range(N):
            if weights[k] == 0:
                SigmaML[k] = Sigma[k]
            else:
                diff = X[k] - X  # محاسبه اختلاف‌ها
                weighted_W = (weights[k] * W_matrix_values[k, :]) / M
                a = np.einsum('i,ij,ik->jk', weighted_W, diff, diff)  # محاسبه a به صورت ماتریسی
                c = np.sum(weighted_W)  # محاسبه c

                if (np.linalg.det(a) > 0) and (c != 0) and np.isfinite(c):
                    SigmaML[k] = a / c  # به روز رسانی Sigma به عنوان ماتریس d * d
                    # بررسی حداقل Sigma
                    if np.linalg.det(SigmaML[k]) < np.linalg.det(MinSigma):
                        SigmaML[k] = MinSigma
                else:
                    SigmaML[k] = Sigma[k]  # اگر محاسبه مشکل داشت، Sigma اولیه استفاده می‌شود

        Sigma = SigmaML  # بروزرسانی Sigma

    return Sigma
