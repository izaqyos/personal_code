const gql = require('graphql');

const {GraphQLObjectType, GraphQLObjectString, GraphQLObjectInt} = gql;

const BookType = new GraphQLObjectType({
    name: 'book',
    fields: () => {
            id: {type: GraphQLObjectString},
    }
});
