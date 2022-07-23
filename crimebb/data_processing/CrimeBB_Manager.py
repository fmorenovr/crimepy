import pandas as pd

class CrimeBBManager():
    
    def __init__(self, data_path, year):
        self.DATA_PATH = data_path
        self.YEAR = year
        self.CSV_PATH = f"{self.DATA_PATH}csv/{self.YEAR}/summary/"
        self.CSV_PROCESSED = f"{self.DATA_PATH}csv/{self.YEAR}/processed/"

    def generates_reading(self, read_direct=False, chunk_size=1000000):
        print("Loading boards ... ")
        boards_df = pd.read_csv(f"{self.CSV_PROCESSED}boards.csv", sep="\t", low_memory=False)
        print("Loading threads ... ")
        threads_df = pd.read_csv(f"{self.CSV_PROCESSED}threads.csv", sep="\t", low_memory=False)

        print("Loading posts ... ")
        if read_direct:
            posts_df = pd.read_csv(f"{self.CSV_PROCESSED}posts.csv", sep="\t", low_memory=False)

            _df = pd.merge(posts_df, threads_df[["site_id", "board_id", "thread_id", "thread_title"]].drop_duplicates(), on=["site_id", "board_id", "thread_id"], how="left")
            _df = pd.merge(_df, boards_df[["site_id", "site_name", "board_id", "board_title"]].drop_duplicates(), on=["site_id", "board_id"], how="left")
            
            print("Creating crimeBB directly ...")
            crimebb_df = _df[['site_id', 'board_id', 'thread_id', 'user_id', 'post_id', 
                              'site_name', 'board_title', 'thread_title', 'username', 'content', 
                              'user_reputation', 'post_data_creation']].copy()

        else:
            posts_reader = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False, iterator=True)
            
            print("Creating crimeBB by iterator ...")
            crimebb_df = pd.DataFrame()
            
            len_readed=chunk_size
            while len_readed>=chunk_size:
                current_df = posts_reader.get_chunk(chunk_size).copy()
                current_df.drop_duplicates(inplace=True)

                _df = pd.merge(posts_df, threads_df[["site_id", "board_id", "thread_id", "thread_title"]].drop_duplicates(), on=["site_id", "board_id", "thread_id"], how="left")
                _df = pd.merge(_df, boards_df[["site_id", "site_name", "board_id", "board_title"]].drop_duplicates(), on=["site_id", "board_id"], how="left")
            
                crimebb_df = pd.concat([crimebb_df, _df], ignore_index=True)
            
                len_readed = current_df.shape[0]
        
        crimebb_df.to_csv(f"{self.CSV_PROCESSED}crimeBB_{self.YEAR}.csv", sep='\t', index=False)
        
        return crimebb_df
    
    ### CRIMEBB 2021 VERSION
    
    def process_members(self):
        members_df = pd.read_csv(f"{self.CSV_PATH}members.csv", sep="\t", low_memory=False)
        members_df.drop_duplicates(inplace=True)
        
        members_df = members_df[["id", "username", "site_id"]].copy().drop_duplicates()
        members_df.rename(columns={"id":"user_id"}, inplace=True)
        members_df.drop_duplicates(inplace=True)

        members_df.to_csv(f"{self.CSV_PROCESSED}members.csv", sep='\t', index=False)
        
        return members_df
    
    def process_sites(self):
        website_df = self.boards_df[["site_id", "site_name"]].copy()
        website_df.drop_duplicates(inplace=True)
        
        website_df.sort_values(by="site_id", inplace=True)

        website_df.to_csv(f"{self.CSV_PROCESSED}sites.csv", sep='\t', index=False)
        
        return website_df
    
    def process_boards(self):
        boards_df = pd.read_csv(f"{self.CSV_PATH}boards.csv", sep="\t", low_memory=False)
        boards_df["url"] = boards_df["url"].apply(lambda x: x.replace("antichat.com", "forum.antichat.ru"))
        boards_df["site_name"] = boards_df["url"].apply(lambda x: (x.replace("https://", "")).split("/")[0] if "https" in x else (x.replace("http://", "")).split("/")[0] )
        boards_df.drop_duplicates(inplace=True)

        #boards_df.drop(columns=["db_created_on", "db_updated_on"], inplace=True)
        #boards_df.drop_duplicates(inplace=True)
        
        boards_df = boards_df[["id", "site_id", "site_name", "name", "url"]].copy().drop_duplicates()
        boards_df.rename(columns={"id":"board_id", 
                                  "name":"board_title", 
                                  "url":"board_url"}, inplace=True)
        boards_df.drop_duplicates(inplace=True)

        #boards_df = boards_df[["board_id", "site_id", "site_name", "board_title", "board_url"]].copy()
        #boards_df.drop_duplicates(inplace=True)

        self.boards_df = boards_df

        boards_df.to_csv(f"{self.CSV_PROCESSED}boards.csv", sep='\t', index=False)
        
        return boards_df
        
    def process_threads(self):
        threads_df = pd.read_csv(f"{self.CSV_PATH}threads.csv", sep="\t", low_memory=False)
        threads_df["url"] = threads_df["url"].apply(lambda x: x.replace("antichat.com", "forum.antichat.ru"))
        threads_df.drop_duplicates(inplace=True)

        #threads_df.drop(columns=["label", "last_post_on", "is_forward_direction", "db_created_on", "db_updated_on", "created_on"], inplace=True)
        #threads_df.drop_duplicates(inplace=True)
        
        threads_df = threads_df[["id", "site_id", "board_id", "creator_id", "creator", "name", "url"]].copy().drop_duplicates()
        threads_df.rename(columns={"creator":"username", 
                                   "id":"thread_id", 
                                   "creator_id":"user_id", 
                                   "name":"thread_title", 
                                   "url":"thread_url"}, inplace=True)
        threads_df.drop_duplicates(inplace=True)

        #threads_df = threads_df[["thread_id", "site_id", "board_id", "user_id", "username", "thread_title", "thread_url"]].copy()
        #threads_df.drop_duplicates(inplace=True)

        threads_df.to_csv(f"{self.CSV_PROCESSED}threads.csv", sep='\t', index=False)
        
        return threads_df
        
    def process_posts(self, read_direct=False, chunk_size=1000000):
    
        if read_direct:

            posts_df = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False)
            posts_df.drop_duplicates(inplace=True)

            posts_df = posts_df[["id", "site_id", "board_id", "thread_id", "creator_id", "creator", "creator_reputation", "content", "created_on"]].copy().drop_duplicates()
            posts_df.rename(columns={"creator":"username", 
                                        "id":"post_id", 
                                        "creator_id":"user_id", 
                                        "creator_reputation":"user_reputation", 
                                        "created_on": "post_data_creation"}, inplace=True)
            posts_df.drop_duplicates(inplace=True)

            #posts_final = posts_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_reputation", "content", "post_data_creation"]].copy().drop_duplicates()
            #posts_final.drop_duplicates(inplace=True)

        else:
            posts_reader = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False, iterator=True)
            
            posts_df = pd.DataFrame()
            
            len_readed=chunk_size
            while len_readed>=chunk_size:
                current_df = posts_reader.get_chunk(chunk_size).copy()
                current_df.drop_duplicates(inplace=True)

                #posts_df.drop(columns=["is_a_reply", "updated_on", "db_created_on", "db_updated_on", "quoted_post_ids", "creator_n_posts"], inplace=True)
                #posts_df.drop_duplicates(inplace=True)

                current_df = current_df[["id", "site_id", "board_id", "thread_id", "creator_id", "creator", "creator_reputation", "content", "created_on"]].copy().drop_duplicates()
                current_df.rename(columns={"creator":"username", 
                                         "id":"post_id", 
                                         "creator_id":"user_id", 
                                         "creator_reputation":"user_reputation", 
                                         "created_on":"post_data_creation"}, inplace=True)
                current_df.drop_duplicates(inplace=True)
            
                posts_df = pd.concat([posts_df, current_df], ignore_index=True)
            
                len_readed = current_df.shape[0]
        
        posts_df.to_csv(f"{self.CSV_PROCESSED}posts.csv", sep='\t', index=False)

        return  posts_df
        

    ### CRIMEBB 2019 VERSION
    
    def process_members_2019(self):
        members_df = pd.read_csv(f"{self.CSV_PATH}members.csv", sep="\t", low_memory=False)
        members_df.drop_duplicates(inplace=True)
        
        members_df = members_df[["IdMember", "Username", "site"]].copy().drop_duplicates()
        members_df.rename(columns={"IdMember":"user_id", 
                                   "Username":"username", 
                                   "site":"site_id"}, inplace=True)
        members_df.drop_duplicates(inplace=True)
        
        members_df = members_df[["user_id", "username", "site_id"]].copy()
        members_df.drop_duplicates(inplace=True)

        members_df.to_csv(f"{self.CSV_PROCESSED}members.csv", sep='\t', index=False)
        
        return members_df

    def process_sites_2019(self):
        website_df = pd.read_csv(f"{self.CSV_PATH}sites.csv", sep="\t", low_memory=False)
        website_df.drop(columns=["NumMembers", "NumForums", "parsed", "Name", "LastParse"], inplace=True)
        website_df.drop_duplicates(inplace=True)
        
        website_df.rename(columns={"URL":"site_name", 
                                   "IdSite":"site_id"}, inplace=True)
        website_df.drop_duplicates(inplace=True)
        
        website_df["site_name"] = website_df["site_name"].apply(lambda x: (x.replace("https://", "")) if "https" in x else (x.replace("http://", "")) )
        website_df.sort_values(by="site_id", inplace=True)
        
        website_df.to_csv(f"{self.CSV_PROCESSED}sites.csv", sep='\t', index=False)
        
        self.website_df = website_df

        return website_df
        
    def process_boards_2019(self):
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
        
        boards_df.to_csv(f"{self.CSV_PROCESSED}boards.csv", sep='\t', index=False)
        
        return boards_df
        
    def process_threads_2019(self):
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
        
        threads_df.to_csv(f"{self.CSV_PROCESSED}threads.csv", sep='\t', index=False)
        
        self.threads_df = threads_df

        return threads_df
        
    def process_posts_2019(self, read_direct=False, chunk_size=1000000):
    
        if read_direct:

            posts_df = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False)
            posts_df.drop_duplicates(inplace=True)

            posts_df.drop(columns=["Likes", "parsed", "LastParse", "CitedPost", "AuthorNumPosts"], inplace=True)
            posts_df.drop_duplicates(inplace=True)

            posts_df.rename(columns={"IdPost": "post_id", 
                                    "Author":"user_id", 
                                    "thread":"thread_id", 
                                    "Timestamp":"post_data_creation", 
                                    "Content":"content", "site":"site_id", 
                                    "AuthorReputation":"user_reputation", 
                                    "site":"site_id", 
                                    "AuthorName":"username"}, inplace=True)
            posts_df.drop_duplicates(inplace=True)
            
            posts_df = pd.merge(posts_df, self.threads_df[["site_id", "board_id", "thread_id"]], how="left", on=["site_id", "thread_id"])
            posts_df.drop_duplicates(inplace=True)

            posts_df = posts_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_reputation", "content", "post_data_creation"]].copy()
            posts_df.drop_duplicates(inplace=True)

        else:
            posts_reader = pd.read_csv(f"{self.CSV_PATH}posts.csv", sep="\t", low_memory=False, iterator=True)
            
            posts_df = pd.DataFrame()
            
            len_readed=chunk_size
            while len_readed>=chunk_size:
                current_df = posts_reader.get_chunk(chunk_size).copy()
                current_df.drop_duplicates(inplace=True)

                current_df.drop(columns=["Likes", "parsed", "LastParse", "CitedPost", "AuthorNumPosts"], inplace=True)
                current_df.drop_duplicates(inplace=True)

                current_df.rename(columns={"IdPost": "post_id", 
                                            "Author":"user_id", 
                                            "thread":"thread_id", 
                                            "Timestamp":"post_data_creation", 
                                            "Content":"content", "site":"site_id", 
                                            "AuthorReputation":"user_reputation", 
                                            "site":"site_id", 
                                            "AuthorName":"username"}, inplace=True)
                current_df.drop_duplicates(inplace=True)
                
                current_df = pd.merge(current_df, self.threads_df[["site_id", "board_id", "thread_id"]], how="left", on=["site_id", "thread_id"])
                current_df.drop_duplicates(inplace=True)

                current_df = current_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_reputation", "content", "post_data_creation"]].copy()
                current_df.drop_duplicates(inplace=True)
            
                posts_df = pd.concat([posts_df, current_df], ignore_index=True)
            
                len_readed = current_df.shape[0]
        
        posts_df.to_csv(f"{self.CSV_PROCESSED}posts.csv", sep='\t', index=False)
        
        return posts_df
