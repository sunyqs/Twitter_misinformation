library(dplyr)
library(tidyr)
library(psych)
data=read.csv("User Study for Misinformation Algorithm.csv")
attach(data)
plot(pre.attitude[condition=="1"],post_attitude[condition=='1'],xbar='pre_attitude',ybar='post_attitude',pch=15, col="green")
points(pre.attitude[condition=='2'],post_attitude[condition=='2'],pch=15, col='red')
points(pre.attitude[condition=='3'],post_attitude[condition=='3'],pch=15, col='blue')
condition=factor(condition)
test=lm(post_attitude~pre.attitude + condition)
anova(test)
test_age=lm(post_attitude~pre.attitude + condition + Q22)
anova(test_age)
test_gender=lm(post_attitude~pre.attitude + condition + Q24)
anova(test_gender)
test_race=lm(post_attitude~pre.attitude + condition + Q26)
anova(test_race)
test_poli=lm(post_attitude~pre.attitude + condition + Q28)
anova(test_poli)
test_all=lm(post_attitude~pre.attitude + condition + Q22 + Q24 + Q26 + Q28, data=data)
anova(test_all)

data=data[data$Q22>=18,]
aov_cred=aov(misinfo_cred~condition, data=data)
summary(aov_cred)
summary.lm(aov_cred)

test_mid=lm(log(post_attitude)~condition + misinfo_cred + log(pre.attitude) + Q22 + Q24 +Q26 +Q28, data=data)
anova(test_mid)
aov_mod=aov(log(post_attitude)~condition * Q28 ,data=data)
summary(aov_mod)
summary.lm(aov_mod)

mis_cred_mean <- data %>% 
  group_by(condition) %>% 
  summarise(
    misinfo_cred = mean(misinfo_cred)
  )

data <- data %>% mutate(condition = factor(condition, levels = c(1, 2, 3), labels = c("Misinformation Only", "Fact Checking Label", "Fack Checking Lable &Reasoning")))
ggplot(mis_cred_mean, aes(x = condition, y = misinfo_cred)) +
  geom_bar(stat = "identity",width=0.5,) +
  labs(
    x = "Condition",
    y = "Percieved Misinformation Credibility"
  )


