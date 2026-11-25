from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://arxiv.org/robots.txt")
rp.read()

print("crawl_delay:", rp.crawl_delay("CourseSpider"))
print("can_fetch abs:", rp.can_fetch("CourseSpider", "https://arxiv.org/abs/1706.03762"))
print("can_fetch search:", rp.can_fetch("CourseSpider", "https://arxiv.org/search/?query=transformer"))