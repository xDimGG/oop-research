import os
from tree_sitter import Node, Tree
from tree_sitter_languages import get_parser
from collections import defaultdict

parser = get_parser('java')

# https://github.com/tree-sitter/py-tree-sitter/issues/33
def traverse_tree(tree: Tree):
	cursor = tree.walk()

	reached_root = False
	while reached_root == False:
		yield cursor.node

		if cursor.goto_first_child():
			continue

		if cursor.goto_next_sibling():
			continue

		retracing = True
		while retracing:
			if not cursor.goto_parent():
				retracing = False
				reached_root = True

			if cursor.goto_next_sibling():
				retracing = False

i = 0

# 2
method_paramter_counts = defaultdict(int)

# 4
class_method_counts = defaultdict(int)

# 5
class_member_counts = defaultdict(int)

# 7
class_uses_inheritance = 0
class_uses_interfaces = 0
class_uses_both = 0
class_uses_neither = 0

def handle_node(node: Node):
	global class_uses_both, class_uses_inheritance, class_uses_interfaces, class_uses_neither
	# print(node.sexp())

	# 2
	if node.type == 'formal_parameters':
		cur = node.walk()
		method_paramter_counts[cur.node.named_child_count] += 1

	# 7
	if node.type == 'class_declaration':
		cur = node.walk()
		cur.goto_first_child()

		uses_inheritance = False
		uses_interfaces = False

		while cur.goto_next_sibling():
			if cur.node.type == 'superclass':
				uses_inheritance = True

			if cur.node.type == 'super_interfaces':
				uses_interfaces = True

		class_uses_both += uses_inheritance and uses_interfaces
		class_uses_inheritance += uses_inheritance
		class_uses_interfaces += uses_interfaces
		class_uses_neither += not uses_inheritance and not uses_interfaces

	if node.type == 'class_body':
		cur = node.walk()
		cur.goto_first_child()

		# 4
		method_count = 0

		# 5
		member_count = 0

		while cur.goto_next_sibling():
			# 4
			if cur.node.type == 'method_declaration':
				method_count += 1

			# 5
			if cur.node.type == 'field_declaration':
				member_count += 1

		class_method_counts[method_count] += 1
		class_member_counts[member_count] += 1

for root, dirs, files in os.walk('repos\\Java'):
	for file in files:
		if file.endswith('.java'):
			i += 1

			with open(os.path.join(root, file), 'rb') as f:
				# if i < 460:
				# 	continue

				src = f.read()
				tree = parser.parse(src)

				for node in traverse_tree(tree):
					handle_node(node)

				# print(src.decode())
				# exit()

			if i == 10000:
				print('(2)', method_paramter_counts)
				print('(4)', class_method_counts)
				print('(5)', class_member_counts)
				print('(7)', class_uses_both, class_uses_inheritance, class_uses_interfaces, class_uses_neither)
				exit()
