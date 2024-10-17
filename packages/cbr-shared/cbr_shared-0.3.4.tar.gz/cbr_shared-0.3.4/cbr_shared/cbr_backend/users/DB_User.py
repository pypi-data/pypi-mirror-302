import re

from botocore.exceptions            import ClientError
from cbr_shared.aws.s3.S3_DB_Base   import S3_DB_Base
from osbot_utils.utils.Http         import url_join_safe
from osbot_utils.utils.Str          import str_safe
from osbot_utils.utils.Json         import json_dumps, json_loads

S3_DB_User__BUCKET_NAME__SUFFIX = "db-users"                       # todo: change this name 'db-users' to something more relevant to S3_DB_Base (since this is a legacy name from the early statges of cbr dev)
S3_DB_User__BUCKET_NAME__PREFIX = 'cyber-boardroom'

S3_FOLDER_NAME__USERS_DATA      = 'users_data'

FILE_NAME__USER__METADATA       = 'metadata.json'
FILE_NAME__USER__PAST_CHATS     = 'past_chats.json'

class DB_User(S3_DB_Base):
    bucket_name__suffix: str = S3_DB_User__BUCKET_NAME__SUFFIX
    bucket_name__prefix: str = S3_DB_User__BUCKET_NAME__PREFIX

    def __init__(self, user_id):
        self.user_id  = str_safe(user_id)
        super().__init__()

    def __enter__(self                        ): return self
    def __exit__ (self, type, value, traceback): pass
    def __repr__ (self                        ): return f"<DB_User: {self.user_id}>"

    def create(self):
        metadata_as_str = json_dumps(self.default_metadata())
        kwargs = dict(file_contents = metadata_as_str,
                      bucket        = self.s3_bucket(),
                      key           = self.s3_key_user_metadata())
        return self.s3().file_create_from_string(**kwargs)

    def delete(self):
        kwargs = dict(bucket        = self.s3_bucket(),
                      key           = self.s3_key_user_metadata())
        return self.s3().file_delete(**kwargs)

    def exists(self):
        return self.s3().file_exists(self.s3_bucket(), self.s3_key_user_metadata())

    def metadata(self):
        try:
            raw_data = self.s3().file_contents(self.s3_bucket(), self.s3_key_user_metadata())
            return json_loads(raw_data)
        except ClientError:
            return {}

    def metadata_update(self, metadata):
        metadata_as_str = json_dumps(metadata)
        kwargs = dict(file_contents = metadata_as_str,
                      bucket        = self.s3_bucket(),
                      key           = self.s3_key_user_metadata())
        return self.s3().file_create_from_string(**kwargs)


    def default_metadata(self):
        return { 'user_id': self.user_id ,
                 'type'   : 'pytest_user'}

    # def s3_folder_user_profile(self, user_id):
    #     return f'{self.s3_folder_user_profiles()}/{user_id}'

    def get_metadata_value(self, key):
        return self.metadata().get(key)

    def s3_folder_users_data(self):
        return S3_FOLDER_NAME__USERS_DATA

    def s3_folder_user_data(self):
        return url_join_safe(self.s3_folder_users_data(),self.user_id )

    def s3_key_user_metadata(self):
        return f'{self.s3_folder_user_data()}/{FILE_NAME__USER__METADATA}'

    def s3_key_user_past_chats(self):
        return f'{self.s3_folder_user_data()}/{FILE_NAME__USER__PAST_CHATS}'

    def set_metadata_value(self, key,value):
        metadata = self.metadata()
        metadata[key] = value
        return self.metadata_update(metadata)

    def set_metadata_values(self, values):
        metadata = self.metadata()
        for key,value in values.items():
            metadata[key] = value
        return self.metadata_update(metadata)

    # user data related methods

    def user_past_chats(self):
        s3_key_past_chats = self.s3_key_user_past_chats()
        if self.s3_file_exists(s3_key_past_chats):
            return self.s3_file_contents_json(s3_key_past_chats)
        return {}

    def user_past_chats__add_chat(self, chat_path):
        safe_chat_path = re.sub(r'[^0-9a-f\-/]', '', chat_path)     # refactor to central location with these regexes
        if safe_chat_path != chat_path:
            return False
        past_chats = self.user_past_chats()
        if 'chat_paths' not in past_chats:
            past_chats['chat_paths'] = []
        past_chats['chat_paths'].append(safe_chat_path)
        return self.s3_save_data(past_chats, self.s3_key_user_past_chats())


    def user_profile(self):
        metadata = self.metadata()
        if metadata:
            if 'cognito_data' in metadata:
                del metadata['cognito_data']
            return metadata
        return {}

