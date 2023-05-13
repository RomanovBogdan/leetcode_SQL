import argparse
import os

import leetcode
import pandas as pd

META_FILE = '.meta.csv'
LANG_SPECS = {
    'SQL': {
        'ext': 'sql',
        'com': '#'
    }
}
SOLUTIONS_DIR = 'solutions'


def _get_title_slugs(problems: list, lang: str, d: str) -> dict:
    slugs = dict()
    for problem in problems:
        if problem.startswith('http'):
            slug = problem
            if problem.endswith('/'):
                slug = slug[:-1].split('/')[-1]
            slugs[slug] = os.path.join(d, f'{slug}.{LANG_SPECS[lang]["ext"]}')
        else:
            slugs[problem] = os.path.join(d, f'{problem}.{LANG_SPECS[lang]["ext"]}')

    existing_solutions = list()
    for k, v in slugs.items():
        if os.path.exists(v):
            print(f'Skipping {k}, {v} already exists.')
            existing_solutions.append(k)
    for i in existing_solutions:
        del slugs[i]

    return slugs


def get_slug_data(name: str) -> dict:
    configuration = leetcode.Configuration()
    configuration.api_key['Referer'] = 'https://leetcode.com'
    configuration.debug = False
    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))
    graphql_request = leetcode.GraphqlQuery(
        query='''
                query getQuestionDetail($titleSlug: String!) {
                  question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    boundTopicId
                    title
                    content
                    translatedTitle
                    difficulty
                    similarQuestions
                    topicTags {
                      name
                      slug
                    }
                    codeSnippets {
                      lang
                      langSlug
                      code
                      __typename
                    }
                    stats
                    codeDefinition
                    hints
                    solution {
                      id
                      canSeeDetail
                      __typename
                    }
                    status
                    sampleTestCase
                    enableRunCode
                    metaData
                    translatedContent
                    judgerAvailable
                    judgeType
                    mysqlSchemas
                    enableTestMode
                    envInfo
                    __typename
                  }
                }
            ''',
        variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=name),
        operation_name='getQuestionDetail',
    )
    return api_instance.graphql_post(body=graphql_request).to_dict()


def _generate_leetcode_readme(data: dict, sol_dir: str):
    header = '## Solutions\n\n'
    problems_table = '|Problem|Difficulty|Solution|\n|-|-|-|\n'

    for problem, meta in data.items():
        solutions_links = f'[{meta["lang"]}](/{sol_dir}/{problem}.{LANG_SPECS[meta["lang"]]["ext"]})'
        problems_table += \
            f'| [{meta["id"]}. {problem.replace("-", " ").capitalize()}](https://leetcode.com/problems/{problem}/) ' \
            f'| {meta["difficulty"]} ' \
            f'| {solutions_links}  |\n'
    readme = header + problems_table
    with open(os.path.join(f'{sol_dir}/..', 'README.md'), 'w') as readme_file:
        readme_file.write(readme)


def _update_meta_file(slug: str, lang: str, slug_data: dict, sol_dir: str) -> None:
    meta_file = os.path.join(sol_dir, META_FILE)
    if not os.path.exists(meta_file):
        with open(meta_file, 'w') as f:
            f.write('slug,id,difficulty,lang\n')
    data = pd.read_csv(meta_file, index_col='slug').to_dict('index')

    # adding new problem or solution
    if slug not in data.keys():
        data[slug] = {
            'id': slug_data['question_frontend_id'],
            'difficulty': slug_data['difficulty'],
            'lang': lang
        }
    else:
        data[slug]['lang'].append(lang)

    pd.DataFrame.from_dict(data).transpose().to_csv(meta_file, index_label='slug', index=True)


def pull(problems: list, lang: str, sol_dir: str):
    slugs = _get_title_slugs(problems, lang, sol_dir)
    if len(slugs) == 0:
        print("Nothing to do")
        return

    for slug, file in slugs.items():
        slug_data = get_slug_data(slug)['data']['question']
        with open(file, 'w'):
            pass
        print(f'File generated for {slug}: file://{os.path.abspath(file)}')
        _update_meta_file(slug, lang, slug_data, sol_dir)

    data = pd.read_csv(
        os.path.join(sol_dir, META_FILE), index_col='slug'
    ).to_dict('index')
    _generate_leetcode_readme(data, sol_dir)


def main():
    parser = argparse.ArgumentParser('Simple tool to manage solutions')
    parser.add_argument('val', default='', type=str, nargs='*', help='Values for a chosen call')
    args = parser.parse_args()
    if not os.path.exists(SOLUTIONS_DIR):
        os.mkdir(SOLUTIONS_DIR)
    pull(args.val, 'SQL', SOLUTIONS_DIR)


if __name__ == '__main__':
    main()
