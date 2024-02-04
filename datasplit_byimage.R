## Data subsetting following imaris batch stats extraction
## To change per file:
#  File path
#  File name
#  Frame to select!


library(readxl)
library(dplyr)
library(stringr)
library(tibble)
library(openxlsx)

cbind.all <- function (...) 
{
  nm <- list(...)
  # list all the components to be bound together
  nm <- lapply(nm, as.matrix)
  n <- max(sapply(nm, nrow))
  # find the max row numbers among the components to be bound together
  do.call(cbind, 
          lapply(nm, 
                 function(x) rbind(x, matrix(0, n - nrow(x), ncol(x)))
                 # the function is to rbind a matrix of NAs with to reach the max.row number
                 ))
}



# Remember to change the pathname
directory_path <- "/Users/UZH-wezhon/Desktop/D12_imaris_analysis/labeledWT_filtered180/fLCD_colocTDP_vol_Statistics"

# Remember to change the filename
filename <- "fLCD_colocTDP_vol_Scatter_Plot_1D"
xlsx <- "xlsx"
csv <- "csv"

# If .xlsx
# df <- read_excel(file.path(directory_path, paste0(filename, ".", xlsx)))
# If .csv
df <-  read.csv(file.path(directory_path, paste0(filename, ".", csv)), skip = 3, header = T)
colnames(df)

# Columns to remove
# columns_to_remove <- c("Original.Component.ID", "Original.Image.ID", "X")

columns_to_keep <- c("Volume", "Original.Image.Name")

# Remove unwant columns 
#df <- df %>% select(-one_of(columns_to_remove))

# Keep only values and image name
df <- df %>% select(all_of(columns_to_keep))

# Define the names and images of the samples
names <- sprintf("B%02d", 2:11)
images <- sprintf("%03d", 1:6)
df_list <- data.frame()
df_temp <- data.frame()
df_list_values <- data.frame()
df_list_names <- data.frame()
df_list_rmoutliers <- data.frame()
df_list_outliers <- data.frame()

for (name in names){
  df_name <- df %>% filter(grepl(name, df[ , 2]))
  for (image in images){
    df_image <- df_name %>% filter(grepl(image, df_name[ , 2]))
    # keep only the value
    df_temp_values <- df_image[1]
    df_temp_names <- df_image[2]
    image_name <- c(name, image)
    colnames(df_temp_values) <- paste(image_name, collapse = '_')
    
    values_nonzero <- subset(df_temp_values, df_temp_values != 0)

    quartiles <- quantile(values_nonzero[, 1], probs=c(.25, .75), na.rm = FALSE)
    IQR <- IQR(df_temp_values[, 1])
    
    Lower <- quartiles[1] - 1.5*IQR
    Upper <- quartiles[2] + 1.5*IQR 
    
    values_no_outlier <- subset(values_nonzero, values_nonzero[, 1] > Lower & values_nonzero[, 1] < Upper)
    values_outlier <- subset(values_nonzero, values_nonzero[, 1] <= Lower | values_nonzero[, 1] >= Upper)
    
    df_list_values <- cbind.all(df_list_values, df_temp_values)
    df_list_rmoutliers <- cbind.all(df_list_rmoutliers, values_no_outlier)
    df_list_outliers <- cbind.all(df_list_outliers, values_outlier)
    df_list_names <- cbind.all(df_list_names, df_temp_names)
  }
}  

df_list_values <- as.data.frame(df_list_values)
stats <- as.data.frame(summary(df_list_values))
counts <- as.data.frame(colSums(df_list_values != 0))
counts_rmoutlier <- as.data.frame(colSums(df_list_rmoutliers != 0))
sums <- as.data.frame(colSums((df_list_values)))
rmoutliers <- as.data.frame(df_list_rmoutliers)
outliers <- as.data.frame(df_list_outliers)


# View(df_list_values)
# View(stats)
# View(counts)


file_path_subset <- file.path(directory_path, paste0(filename, "_subset", ".", xlsx))
subsetted <- createWorkbook()
addWorksheet(subsetted, sheetName = "Values")
addWorksheet(subsetted, sheetName = "Image names")
# Write subsetted data Value/Names to the respective sheets
writeData(subsetted, sheet = "Values", x = df_list_values)
writeData(subsetted, sheet = "Image names", x = df_list_names)
saveWorkbook(subsetted, file_path_subset, overwrite=T)


file_path_stats <- file.path(directory_path, paste0(filename, "_stats", ".", xlsx))
file_path_counts <- file.path(directory_path, paste0(filename, "_counts", ".", xlsx))
file_path_counts_rmoutliers <- file.path(directory_path, paste0(filename, "_counts_rmoutliers", ".", xlsx))
file_path_sums <- file.path(directory_path, paste0(filename, "_sum", ".", xlsx))
file_path_rmoutliers <- file.path(directory_path, paste0(filename, "_rmoutliers", ".", xlsx))
file_path_outliers <- file.path(directory_path, paste0(filename, "_outliers", ".", xlsx))

write.xlsx(stats, file_path_stats, rowNames = TRUE)
write.xlsx(counts, file_path_counts, rowNames = TRUE)
write.xlsx(counts_rmoutlier, file_path_counts_rmoutliers, rowNames = TRUE)
write.xlsx(sums, file_path_sums, rowNames = TRUE)
write.xlsx(rmoutliers, file_path_rmoutliers, rowNames = TRUE)
write.xlsx(outliers, file_path_outliers, rowNames = TRUE)















