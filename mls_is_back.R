library(tidyr)
library(dplyr)

df <- read.csv("soccer-spi/spi_global_rankings.csv")
groups <- read.csv("groups.csv")

group_lookup <- groups %>% 
  pivot_longer(colnames(groups), names_to = "group", values_to = "name") %>%
  mutate_all(.funs=tolower) %>%
  na_if("") %>%
  na.omit

mls <- df %>%
  filter(league == "Major League Soccer") %>%
  select("rank", "name", "spi", "off", "def") %>%
  mutate_all(.funs=tolower) %>%
  full_join(group_lookup)

twelve = NULL
third = NULL
for (val in unique(mls$group)) {
  twelve = rbind(twelve, filter(mls, group == val)[1:2,])
  third = rbind(third, filter(mls, group == val)[3:3,])
}

# naive approach: add next 4 best
# sixteen <- rbind(twelve, third[1:4,])

# advanced approach: incorporate others in group somehow
avg <- mls %>% 
  group_by(group) %>% 
  summarize(avg = mean(as.numeric(spi))) %>%
  right_join(third)

avg$diff <- (as.numeric(avg$spi) - as.numeric(avg$avg))
sixteen <- full_join(twelve, avg[order(-avg$diff),][1:4,])

write.csv(sixteen[order(sixteen$group),], file = "mls_is_back.csv")
