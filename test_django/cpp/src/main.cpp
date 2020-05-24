#include <iostream>
#include "curl/curl.h"

class CURL {
public:
  static bool init();
  static bool setopt(CURLoption opts...);


private:
  static CURL s_curl;
  CURL* m_curl = nullptr;
};

class CURL_Server {

}


int main() {
  CURLcode ret = curl_global_init(CURL_GLOBAL_ALL);

  if(ret != CURLE_OK) {
    std::cerr << "cURL failed to initialize (curl_global_init): " << ret << std::endl;
    return -1;
  }

  CURL* curl = curl_easy_init();

  if(!curl) {
    std::cerr << "cURL failed to initialize (curl_easy_init)" << std::endl;
    return -1;
  }

  curl_easy_setopt(curl, )


  return 0;
}