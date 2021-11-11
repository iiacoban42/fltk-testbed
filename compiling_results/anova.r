
library(lme4)
library(lmerTest)
library(readr)

# read in data from 4-way ANOVA with between-subject and within-subject factors
df_full <- read_csv("compiling_results/exp_data.csv")

# get parameter estimates from a linear regression with random effects
my_model_fit <- lmer(Code_Size ~ Processors * Workloads + (Processors|Workloads), df_full)
# display results of linear regression
summary(my_model_fit)

# main and interaction effects
anova(my_model_fit)
# random effects
rand(my_model_fit)
# access underlying model for fixed effects
my_glm_fe = model.matrix(my_model_fit)
# access underlying model for random effects
my_glm_re = getME(my_model_fit, "Zt")
# inspect matrices
image(t(my_glm_fe))
image(t(my_glm_re))