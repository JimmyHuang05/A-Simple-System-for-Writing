import json
import os
import random
import string

class BookManager:
    def __init__(self):
        self.books = []
        self.data_folder = "data"  # 数据文件夹路径
        self.book_folder = os.path.join(self.data_folder, "books.json")  # 作品信息文件路径
        self.load_books()  # 加载已保存的图书信息
        self.display_books()  # 程序启动时自动显示所有作品

    def load_books(self):
        """从文件中加载图书信息"""
        if os.path.exists(self.book_folder):
            with open(self.book_folder, "r", encoding="utf-8") as file:
                self.books = json.load(file)
            print("已加载保存的图书信息。")
        else:
            print("未找到保存的图书信息，将创建新的存储文件。")

    def save_books(self):
        """将图书信息保存到文件"""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        with open(self.book_folder, "w", encoding="utf-8") as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)
        print("图书信息已保存到文件。")

    def generate_random_code(self):
        """生成随机的8位中英混合代码"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=8))

    def create_book(self):
        print("\n创建新作品")
        title = input("请输入作品名: ")
        description = input("请输入作品简介: ")
        book_code = self.generate_random_code()
        book_folder = os.path.join(self.data_folder, book_code)
        os.makedirs(book_folder)  # 创建作品文件夹
        book = {"作品名": title, "作品简介": description, "作品代码": book_code, "章节": []}
        self.books.append(book)
        self.save_books()  # 创建图书后立即保存
        print(f"作品创建成功！作品代码为：{book_code}")
        self.display_books()

    def display_books(self):
        """显示所有作品"""
        if not self.books:
            print("\n暂无作品信息。")
        else:
            print("\n作品列表：")
            for index, book in enumerate(self.books, start=1):
                print(f"{index}. 作品名: {book['作品名']}, 作品简介: {book['作品简介']}, 作品代码: {book['作品代码']}")
        self.book_menu()

    def book_menu(self):
        """作品管理菜单"""
        while True:
            print("\n请选择操作：")
            print("1. 创建新作品")
            print("2. 管理作品章节")
            print("3. 删除作品")
            choice = input("请输入操作编号 (1/2/3): ")
            if choice == "1":
                self.create_book()
            elif choice == "2":
                self.manage_chapters()
            elif choice == "3":
                self.delete_book()
            else:
                print("无效的输入，请重新选择。")

    def manage_chapters(self):
        """管理作品章节"""
        if not self.books:
            print("\n暂无作品信息，无法管理章节。")
            return

        try:
            book_index = int(input("\n请输入要管理章节的作品序号: ")) - 1
            if 0 <= book_index < len(self.books):
                self.display_chapters(book_index)
                self.chapter_menu(book_index)
            else:
                print("无效的作品序号，请重新选择。")
        except ValueError:
            print("请输入有效的数字序号。")

    def chapter_menu(self, book_index):
        """章节管理菜单"""
        while True:
            print(f"\n管理作品：{self.books[book_index]['作品名']}")
            print("1. 显示所有章节")
            print("2. 增加章节")
            print("3. 修改章节内容")
            print("4. 删除章节")
            print("5. 返回上一级")
            choice = input("请选择操作 (1/2/3/4/5): ")

            if choice == "1":
                self.display_chapters(book_index)
            elif choice == "2":
                self.add_chapter(book_index)
            elif choice == "3":
                self.edit_chapter(book_index)
            elif choice == "4":
                self.delete_chapter(book_index)
            elif choice == "5":
                break
            else:
                print("无效的输入，请重新选择。")

    def display_chapters(self, book_index):
        """显示作品的所有章节"""
        book = self.books[book_index]
        if not book["章节"]:
            print("\n该作品暂无章节。")
        else:
            print("\n章节列表：")
            for index, chapter in enumerate(book["章节"], start=1):
                print(f"{index}. {chapter['章节标题']}")

    def add_chapter(self, book_index):
        """增加章节"""
        print("\n增加新章节")
        title = input("请输入章节标题: ")
        content = input("请输入章节正文: ")
        book_code = self.books[book_index]["作品代码"]
        chapter_file = os.path.join(self.data_folder, book_code, f"{title}.txt")
        with open(chapter_file, "w", encoding="utf-8") as file:
            file.write(f"#标题\n{title}\n##正文\n{content}")
        chapter = {"章节标题": title, "章节文件": chapter_file}
        self.books[book_index]["章节"].append(chapter)
        self.save_books()
        print("章节添加成功！")
        self.display_chapters(book_index)

    def edit_chapter(self, book_index):
        """修改章节内容"""
        book = self.books[book_index]
        if not book["章节"]:
            print("\n该作品暂无章节，无法修改。")
            return

        self.display_chapters(book_index)  # 显示当前作品的所有章节
        try:
            chapter_index = int(input("\n请输入要修改的章节序号: ")) - 1
            if 0 <= chapter_index < len(book["章节"]):
                self.chapter_edit_menu(book_index, chapter_index)  # 进入章节编辑菜单
            else:
                print("无效的章节序号，请重新选择。")
        except ValueError:
            print("请输入有效的数字序号。")

    def chapter_edit_menu(self, book_index, chapter_index):
        """章节编辑菜单"""
        while True:
            print(
                f"\n正在编辑作品：{self.books[book_index]['作品名']} 的章节：{self.books[book_index]['章节'][chapter_index]['章节标题']}")
            print("1. 修改章节标题")
            print("2. 修改章节正文")
            print("3. 返回上一级")
            choice = input("请选择操作 (1/2/3): ")

            if choice == "1":
                self.edit_chapter_title(book_index, chapter_index)
            elif choice == "2":
                self.edit_chapter_body(book_index, chapter_index)
            elif choice == "3":
                break
            else:
                print("无效的输入，请重新选择。")

    def edit_chapter_title(self, book_index, chapter_index):
        """修改章节标题"""
        book = self.books[book_index]
        chapter = book["章节"][chapter_index]
        new_title = input("请输入新的章节标题: ").strip()
        if new_title:
            chapter["章节标题"] = new_title
            chapter_file = chapter["章节文件"]
            with open(chapter_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
            lines[1] = f"{new_title}\n"  # 更新标题行
            with open(chapter_file, "w", encoding="utf-8") as file:
                file.writelines(lines)
            print("章节标题修改成功！")
            self.display_chapters(book_index)

    def edit_chapter_body(self, book_index, chapter_index):
        """修改章节正文"""
        book = self.books[book_index]
        chapter = book["章节"][chapter_index]
        chapter_file = chapter["章节文件"]
        with open(chapter_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        body_start = lines.index("##正文\n") + 1
        original_body = "".join(lines[body_start:]).strip()  # 获取原始正文内容
        print("当前章节正文内容：")
        print(original_body)  # 打印原始正文内容
        new_body = input("请输入新的章节正文: ").strip()
        if new_body:  # 确保用户输入了新的内容
            lines[body_start:] = [new_body + "\n"]
            with open(chapter_file, "w", encoding="utf-8") as file:
                file.writelines(lines)
            print("章节正文修改成功！")
        else:
            print("未输入新的章节正文，未做修改。")
        self.display_chapters(book_index)

    def delete_chapter(self, book_index):
        """删除章节"""
        book = self.books[book_index]
        if not book["章节"]:
            print("\n该作品暂无章节，无法删除。")
            return

        self.display_chapters(book_index)  # 显示当前作品的所有章节
        try:
            chapter_index = int(input("\n请输入要删除的章节序号: ")) - 1
            if 0 <= chapter_index < len(book["章节"]):
                chapter = book["章节"][chapter_index]
                chapter_file = chapter["章节文件"]
                os.remove(chapter_file)  # 删除章节文件
                book["章节"].pop(chapter_index)  # 从列表中移除章节
                self.save_books()  # 保存更新后的书籍信息
                print("章节删除成功！")
                self.display_chapters(book_index)  # 显示更新后的章节列表
            else:
                print("无效的章节序号，请重新选择。")
        except ValueError:
            print("请输入有效的数字序号。")
        except IndexError:
            print("章节序号超出范围，请重新选择。")

    def delete_book(self):
        """删除作品"""
        if not self.books:
            print("\n暂无作品信息，无法删除。")
            return

        try:
            book_index = int(input("\n请输入要删除的作品序号: ")) - 1
            if 0 <= book_index < len(self.books):
                book_code = self.books[book_index]["作品代码"]
                book_folder = os.path.join(self.data_folder, book_code)
                if os.path.exists(book_folder):
                    for file in os.listdir(book_folder):
                        os.remove(os.path.join(book_folder, file))
                    os.rmdir(book_folder)
                del self.books[book_index]
                self.save_books()
                print("作品删除成功！")
                self.display_books()
            else:
                print("无效的作品序号，请重新选择。")
        except ValueError:
            print("请输入有效的数字序号。")

if __name__ == "__main__":
    manager = BookManager()