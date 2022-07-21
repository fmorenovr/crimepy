import pandas as pd

class CrimeBBManager():
    
    def __init__(self, data_path, year):
        self.DATA_PATH = data_path
        self.YEAR = year
        self.CSV_PATH = f"{self.DATA_PATH}csv/{self.YEAR}/summary/"
        self.CSV_PROCESSED = f"{self.DATA_PATH}csv/{self.YEAR}/processed/"
    
    ### CRIMEBB 2021 VERSION
    
    def read_members(self):
        members_df = pd.read_csv(f"{self.CSV_PATH}members.csv", sep="\t", low_memory=False)
        members_df.drop_duplicates(inplace=True)
        
        self.members_df = members_df
    
    def read_sites(self):
        website_df = self.boards_df[["site_id", "site_name"]].copy()
        website_df.drop_duplicates(inplace=True)
        
        website_df.sort_values(by="site_id", inplace=True)
        
        self.website_df = website_df
    
    def read_boards(self):
        boards_df = pd.read_csv(f"{self.CSV_PATH}boards.csv", sep="\t", low_memory=False)
        boards_df["url"] = boards_df["url"].apply(lambda x: x.replace("antichat.com", "forum.antichat.ru"))
        boards_df["site_name"] = boards_df["url"].apply(lambda x: (x.replace("https://", "")) if "https" in x else (x.replace("http://", "")) )
        boards_df.drop_duplicates(inplace=True)

        boards_df.drop(columns=["db_created_on", "db_updated_on"], inplace=True)
        boards_df.drop_duplicates(inplace=True)

        boards_df.rename(columns={"id":"board_id", 
                                  "name":"board_title", 
                                  "url":"board_url"}, inplace=True)
        boards_df.drop_duplicates(inplace=True)

        boards_df = boards_df[["board_id", "site_id", "site_name", "board_title", "board_url"]].copy()
        boards_df.drop_duplicates(inplace=True)
        
        self.boards_df = boards_df
        
    def read_threads(self):
        threads_df = pd.read_csv(f"{self.CSV_PATH}threads.csv", sep="\t", low_memory=False)
        threads_df["url"] = threads_df["url"].apply(lambda x: x.replace("antichat.com", "forum.antichat.ru"))
        threads_df.drop_duplicates(inplace=True)

        threads_df.drop(columns=["label", "last_post_on", "is_forward_direction", "db_created_on", "db_updated_on", "created_on"], inplace=True)
        threads_df.drop_duplicates(inplace=True)

        threads_df.rename(columns={"creator":"username", 
                                   "id":"thread_id", 
                                   "creator_id":"user_id", 
                                   "name":"thread_title", 
                                   "url":"thread_url"}, inplace=True)
        threads_df.drop_duplicates(inplace=True)

        threads_df = threads_df[["thread_id", "site_id", "board_id", "user_id", "username", "thread_title", "thread_url"]].copy()
        threads_df.drop_duplicates(inplace=True)

        self.threads_df = threads_df
        
    def read_posts(self, chunk_size=1000000):
        #posts_df = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False)
        posts_reader = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False, iterator=True)
        
        posts_final = pd.DataFrame()
        
        len_readed=chunk_size
        while len_readed>=chunk_size:
            posts_df = posts_reader.get_chunk(chunk_size).copy()
            
            posts_df.drop_duplicates(inplace=True)

            posts_df.drop(columns=["is_a_reply", "updated_on", "db_created_on", "db_updated_on", "CitedPost"], inplace=True)
            posts_df.drop_duplicates(inplace=True)

            posts_df.rename(columns={"creator":"username", 
                                     "id":"post_id", 
                                     "creator_id":"user_id", 
                                     "creator_n_posts":"user_num_posts", 
                                     "creator_reputation":"user_reputation", 
                                     "created_on":"post_data_creation"}, inplace=True)
            posts_df.drop_duplicates(inplace=True)

            posts_df = posts_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_num_posts", "user_reputation", "content", "post_data_creation"]].copy()
            posts_df.drop_duplicates(inplace=True)
        
            posts_final = pd.concat([posts_final, posts_df], ignore_index=True)
        
            len_readed = posts_df.shape[0]
        
        self.posts_df = posts_final    

    def generates(self):
        _df = pd.merge(self.posts_df, self.website_df, how="left", on="site_id")
        _df = pd.merge(_df, self.boards_df[["site_id", "board_id", "board_title"]].drop_duplicates(), on=["site_id", "board_id"], how="left")
        _df = pd.merge(_df, self.threads_df[["site_id", "board_id", "thread_id", "thread_title"]].drop_duplicates(), on=["site_id", "board_id", "thread_id"], how="left")
        
        self.crimebb_df = _df[['site_id', 'board_id', 'thread_id', 'user_id', 'post_id', 
                               'site_name', 'board_title', 'thread_title', 'username', 'content', 
                               'user_num_posts', 'user_reputation', 'post_data_creation']].copy()
        
        self.crimebb_df.to_csv(f"{self.CSV_PROCESSED}crimebb_{YEAR}.csv", sep='\t', index=False)
        

    ### CRIMEBB 2019 VERSION

    def read_sites_2019(self):
        website_df = pd.read_csv(f"{self.CSV_PATH}sites.csv", sep="\t", low_memory=False)
        website_df.drop(columns=["NumMembers", "NumForums", "parsed", "Name", "LastParse"], inplace=True)
        website_df.drop_duplicates(inplace=True)
        
        website_df.rename(columns={"URL":"site_name", 
                                   "IdSite":"site_id"}, inplace=True)
        website_df.drop_duplicates(inplace=True)
        
        website_df["site_name"] = website_df["site_name"].apply(lambda x: (x.replace("https://", "")) if "https" in x else (x.replace("http://", "")) )
        website_df.sort_values(by="site_id", inplace=True)
        
        self.website_df = website_df
        
    def read_boards_2019(self):
        boards_df = pd.read_csv(f"{self.CSV_PATH}boards.csv", sep="\t", low_memory=False)
        boards_df.drop_duplicates(inplace=True)
        
        boards_df.drop(columns=["NumThreads", "parsed", "NumPages", "LastParse"], inplace=True)
        boards_df.drop_duplicates(inplace=True)
        
        boards_df.rename(columns={"IdForum":"board_id", 
                                  "Title":"board_title", 
                                  "URL":"board_url", 
                                  "site": "site_id"}, inplace=True)
        boards_df.drop_duplicates(inplace=True)
        
        boards_df = pd.merge(boards_df, self.website_df, how="left", on="site_id")
        boards_df = boards_df[["board_id", "site_id", "site_name", "board_title", "board_url"]].copy()
        boards_df.drop_duplicates(inplace=True)
        
        self.boards_df = boards_df
        
    def read_threads_2019(self):
        threads_df = pd.read_csv(f"{self.CSV_PATH}threads.csv", sep="\t", low_memory=False)
        threads_df.drop_duplicates(inplace=True)
        
        threads_df.drop(columns=["LastParse", "parsed", "NumPages", "Direction", "NumPosts"], inplace=True)
        threads_df.drop_duplicates(inplace=True)
        
        threads_df.rename(columns={"IdThread":"thread_id", 
                                   "site":"site_id", 
                                   "forum":"board_id", 
                                   "Author":"user_id", 
                                   "AuthorName":"username", 
                                   "Heading":"thread_title", 
                                   "URL":"thread_url"}, inplace=True)
        threads_df.drop_duplicates(inplace=True)
        
        threads_df = threads_df[["thread_id", "site_id", "board_id", "user_id", "username", "thread_title", "thread_url"]].copy()
        threads_df.drop_duplicates(inplace=True)
        
        self.threads_df = threads_df
        
    def read_posts_2019(self, chunk_size=1000000):
        #posts_df = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False)
        posts_reader = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False, iterator=True)
        
        posts_final = pd.DataFrame()
        
        len_readed=chunk_size
        while len_readed>=chunk_size:
            posts_df = posts_reader.get_chunk(chunk_size).copy()
            posts_df.drop_duplicates(inplace=True)

            posts_df.drop(columns=["Likes", "parsed", "LastParse", "CitedPost"], inplace=True)
            posts_df.drop_duplicates(inplace=True)

            posts_df.rename(columns={"IdPost": "post_id", 
                                     "Author":"user_id", 
                                     "thread":"thread_id", 
                                     "Timestamp":"post_data_creation", 
                                     "Content":"content", "site":"site_id", 
                                     "AuthorNumPosts":"user_num_posts", 
                                     "AuthorReputation":"user_reputation", 
                                     "site":"site_id", 
                                     "AuthorName":"username"}, inplace=True)
            posts_df.drop_duplicates(inplace=True)
            
            posts_df = pd.merge(posts_df, self.threads_df[["site_id", "board_id", "thread_id"]], how="left", on=["site_id", "thread_id"])
            posts_df.drop_duplicates(inplace=True)

            posts_df = posts_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_num_posts", "user_reputation", "content", "post_data_creation"]].copy()
            posts_df.drop_duplicates(inplace=True)
        
            posts_final = pd.concat([posts_final, posts_df], ignore_index=True)
        
            len_readed = posts_df.shape[0]
        
        self.posts_df = posts_final
        
