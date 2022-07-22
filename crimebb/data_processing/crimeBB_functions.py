import pandas as pd

def generates(CSV_PROCESSED, website_df, boards_df, threads_df, posts_df):
    _df = pd.merge(posts_df, website_df, how="left", on="site_id")
    _df = pd.merge(_df, boards_df[["site_id", "board_id", "board_title"]].drop_duplicates(), on=["site_id", "board_id"], how="left")
    _df = pd.merge(_df, threads_df[["site_id", "board_id", "thread_id", "thread_title"]].drop_duplicates(), on=["site_id", "board_id", "thread_id"], how="left")

    crimebb_df = _df[['site_id', 'board_id', 'thread_id', 'user_id', 'post_id', 
                        'site_name', 'board_title', 'thread_title', 'username', 'content', 
                        'user_reputation', 'post_data_creation']].copy()
    
    crimebb_df.to_csv(f"{CSV_PROCESSED}crimebb.csv", sep='\t', index=False)
    
    return crimebb_df

### CRIMEBB 2021 VERSION

def read_members(CSV_PATH):
    members_df = pd.read_csv(f"{CSV_PATH}members.csv", sep="\t", low_memory=False)
    members_df.drop_duplicates(inplace=True)
    
    return members_df

def read_sites(boards_df):
    website_df = boards_df[["site_id", "site_name"]].copy()
    website_df.drop_duplicates(inplace=True)
    
    website_df.sort_values(by="site_id", inplace=True)
        
    return website_df

def read_boards(CSV_PATH):
    boards_df = pd.read_csv(f"{CSV_PATH}boards.csv", sep="\t", low_memory=False)
    boards_df["url"] = boards_df["url"].apply(lambda x: x.replace("antichat.com", "forum.antichat.ru"))
    boards_df["site_name"] = boards_df["url"].apply(lambda x: (x.replace("https://", "")) if "https" in x else (x.replace("http://", "")) )
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
    
    return boards_df
    
def read_threads(CSV_PATH):
    threads_df = pd.read_csv(f"{CSV_PATH}threads.csv", sep="\t", low_memory=False)
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

    return threads_df
    
def read_posts(CSV_PATH, read_direct=True, chunk_size=1000000):

    if read_direct:
        posts_final = pd.read_csv(f"{CSV_PATH}posts.csv", sep="\t", low_memory=False)
        posts_final.drop_duplicates(inplace=True)

        posts_final = posts_final[["id", "site_id", "board_id", "thread_id", "creator_id", "creator", "creator_reputation", "content", "created_on"]].copy().drop_duplicates()
        posts_final.rename(columns={"creator":"username", 
                                    "id":"post_id", 
                                    "creator_id":"user_id", 
                                    "creator_reputation":"user_reputation", 
                                    "created_on": "post_data_creation"}, inplace=True)
        posts_final.drop_duplicates(inplace=True)

        #posts_final = posts_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_reputation", "content", "post_data_creation"]].copy().drop_duplicates()
        #posts_final.drop_duplicates(inplace=True)

    else:
        posts_reader = pd.read_csv(f"{CSV_PATH}posts.csv", sep="\t", low_memory=False, iterator=True)
        
        posts_final = pd.DataFrame()
        
        len_readed=chunk_size
        while len_readed>=chunk_size:
            posts_df = posts_reader.get_chunk(chunk_size).copy()
            posts_df.drop_duplicates(inplace=True)

            #posts_df.drop(columns=["is_a_reply", "updated_on", "db_created_on", "db_updated_on", "quoted_post_ids", "creator_n_posts"], inplace=True)
            #posts_df.drop_duplicates(inplace=True)

            posts_df = posts_final[["id", "site_id", "board_id", "thread_id", "creator_id", "creator", "creator_reputation", "content", "created_on"]].copy().drop_duplicates()
            posts_df.rename(columns={"creator":"username", 
                                        "id":"post_id", 
                                        "creator_id":"user_id", 
                                        "creator_reputation":"user_reputation", 
                                        "created_on":"post_data_creation"}, inplace=True)
            posts_df.drop_duplicates(inplace=True)

            posts_df = posts_df[["post_id", "site_id", "board_id", "thread_id", "user_id", "username", "user_reputation", "content", "post_data_creation"]].copy()
            posts_df.drop_duplicates(inplace=True)
        
            posts_final = pd.concat([posts_final, posts_df], ignore_index=True)
        
            len_readed = posts_df.shape[0]
    
    return  posts_final